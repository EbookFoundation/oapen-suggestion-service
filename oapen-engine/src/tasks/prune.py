import concurrent.futures
import multiprocessing
import signal
import sys
import threading
import time
from collections import Counter
from threading import Lock
from typing import List

import config
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from model.oapen_types import NgramRow, SuggestionRow
from model.stopwords_processor import STOPWORDS
from prune_tasks.db_task import db_task
from prune_tasks.ngrams_task import ngrams_task
from prune_tasks.reharvest_task import reharvest_task
from tasks.generate_suggestions import get_ngrams_list, suggestion_task
from tqdm.auto import tqdm

connection = get_connection()
db = OapenDB(connection)


def shutdown():
    logger.info("Stopping import.")
    close_connection(connection)


def signal_handler(signal, frame):
    logger.warning("Received shutdown for prune.py.")
    shutdown()
    sys.exit(0)


def run():
    db_mutex = Lock()

    # Find the new stopwords since previous run
    new_stopwords = [sw[0] for sw in db.get_new_stopwords(STOPWORDS)]
    # Update the stopwords table
    db.update_stopwords(STOPWORDS)

    if not new_stopwords == None or len(new_stopwords) == 0:
        logger.info("Added {} new stopwords.".format(len(new_stopwords)))

        # Get the handles of all items with ngrams containing the new stopwords
        logger.info("Searching existing items for added stopwords...")
        refresh_handles = db.get_all_items_containing_stopwords(new_stopwords)
        logger.info(
            "Found {} items with ngrams containing stopwords.".format(
                len(refresh_handles)
            )
        )

        # Re-harvest the bitstreams for those items
        manager = multiprocessing.Manager()
        item_queue = multiprocessing.JoinableQueue(config.IO_MAX_WORKERS * 2)
        db_queue = multiprocessing.JoinableQueue()
        ngrams_event = manager.Event()
        db_event = threading.Event()

        counter = Counter(items_found=0, ngrams_generated=0, items_inserted=0)
        producers_done, consumers_done = 0, 0
        producer_futures = []
        consumer_futures = []
        db_futures = []

        signal.signal(signal.SIGINT, signal_handler)

        pbar = tqdm(
            total=len(refresh_handles),
            desc="Re-harvest Threads Completed",
            mininterval=0,
            miniters=1,
            initial=0,
        )
        pbar.set_postfix({"items found": counter["items_found"]})

        time_start = time.perf_counter()

        ngrams_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=multiprocessing.cpu_count()
        )
        io_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=config.IO_MAX_WORKERS
        )
        db_executor = concurrent.futures.ThreadPoolExecutor()

        for _ in range(multiprocessing.cpu_count()):
            consumer_futures.append(
                ngrams_executor.submit(ngrams_task, item_queue, db_queue, ngrams_event)
            )

        logger.info("Spawned {} ngrams processes.".format(len(consumer_futures)))

        db_futures.append(db_executor.submit(db_task, db, db_queue, db_event))

        def refresh(future, pbar, counter):
            pbar.update(1)
            counter["items_found"] += future.result()
            pbar.set_postfix({"items found": counter["items_found"]})
            pbar.refresh()

        for handle in refresh_handles:
            future = io_executor.submit(reharvest_task, handle, item_queue)
            future.add_done_callback(lambda x: refresh(x, pbar, counter))
            producer_futures.append(future)
            time.sleep(config.HARVEST_THREAD_SPAWN_DELAY)

        for future in concurrent.futures.as_completed(producer_futures):
            producers_done += 1

        if producers_done == len(producer_futures) or io_executor._shutdown:
            item_queue.join()
            ngrams_event.set()
            db_event.set()

        for future in concurrent.futures.as_completed(consumer_futures):
            res = future.result()
            consumers_done += 1
            counter["ngrams_generated"] += res

        db_queue.join()
        ngrams_executor.shutdown(wait=True)
        db_executor.shutdown(wait=True)
        io_executor.shutdown()

        pbar.close()

        logger.info("Completed {0} items".format(counter["ngrams_generated"]))
        logger.info(
            "Reharvest finished in " + str(time.perf_counter() - time_start) + "s."
        )

        # Rerun generate_suggestions on the flagged items
        refresh_items: List[NgramRow] = db.get_ngrams_with_handles(refresh_handles)

        logger.info(
            "Regenerating suggestions for {} items...".format(len(refresh_handles))
        )

        # Necessary to get all items, to run comparisons
        all_items: List[NgramRow] = db.get_all_ngrams(get_empty=False)

        suggestions_futures = []

        # Get only top k ngrams for all items before processing
        for item in all_items:
            ngrams = get_ngrams_list(item)
            item = (item[0], ngrams)

        time_start_suggestions = time.perf_counter()

        n = config.SUGGESTIONS_MAX_ITEMS

        chunks = [refresh_items[i : i + n] for i in range(0, len(refresh_items), n)]

        suggestions_counter = Counter(items_updated=0)

        suggestions_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=config.SUGGESTIONS_MAX_WORKERS
        )

        def refresh_suggestion_pbar(future, counter, pbar):
            pbar.update(future.result())
            counter["items_updated"] += future.result()
            pbar.refresh()

        pbar = tqdm(
            total=len(refresh_items),
            mininterval=0,
            miniters=1,
            leave=True,
            position=0,
            initial=0,
        )

        for chunk in chunks:
            future = suggestions_executor.submit(
                suggestion_task, chunk, all_items, db_mutex, db
            )
            future.add_done_callback(
                lambda x: refresh_suggestion_pbar(x, suggestions_counter, pbar)
            )
            suggestions_futures.append(future)

        for future in concurrent.futures.as_completed(suggestions_futures):
            pass

        logger.info(
            "Updated suggestions for "
            + str(suggestions_counter["items_updated"])
            + " items in "
            + str(time.perf_counter() - time_start_suggestions)
            + "s."
        )

        suggestions_executor.shutdown(wait=True)

        pbar.close()
    else:
        logger.info("No new stopwords, aborting suggestion re-run.")
    # Close the database connection no matter what
    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
