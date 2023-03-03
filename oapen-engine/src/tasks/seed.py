import concurrent.futures
import multiprocessing
import signal
import sys
import threading
import time

import config
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from seed_tasks.db_task import db_task
from seed_tasks.harvest_task import harvest_task
from seed_tasks.ngrams_task import ngrams_task
from tqdm.auto import tqdm

connection = get_connection()
db = OapenDB(connection)


def shutdown():
    logger.info("Stopping import.")
    close_connection(connection)


def signal_handler(signal, frame):
    logger.warning("Received shutdown for seed.py.")
    shutdown()
    sys.exit(0)


def run():
    manager = multiprocessing.Manager()

    item_queue = multiprocessing.JoinableQueue()
    db_queue = multiprocessing.JoinableQueue()

    ngrams_event = manager.Event()
    db_event = threading.Event()

    items_produced, producers_done, consumers_done, items_finished = 0, 0, 0, 0
    producer_futures = []
    consumer_futures = []
    db_futures = []

    urls = db.get_incomplete_urls()

    signal.signal(signal.SIGINT, signal_handler)

    pbar = tqdm(
        total=len(urls),
        desc="Harvest Threads Completed",
        mininterval=0,
        miniters=1,
        initial=0,
    )
    pbar.set_postfix({"items found": items_produced})

    logger.info("Getting items for OapenDB...")
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

    # Start db thread to keep inserting as ngrams are generated
    db_futures.append(db_executor.submit(db_task, db, db_queue, db_event))

    def refresh(future, pbar):
        pbar.update(1)
        pbar.set_postfix({"items found": items_produced})
        pbar.refresh()

    for url in urls:
        future = io_executor.submit(harvest_task, url[0], item_queue)
        future.add_done_callback(lambda x: refresh(x, pbar))
        producer_futures.append(future)
        time.sleep(config.HARVEST_THREAD_SPAWN_DELAY)

    for future in concurrent.futures.as_completed(producer_futures):
        items_produced += future.result()
        producers_done += 1

    if producers_done == len(producer_futures) or io_executor._shutdown:
        item_queue.join()
        ngrams_event.set()
        db_event.set()

    for future in concurrent.futures.as_completed(consumer_futures):
        res = future.result()
        consumers_done += 1
        items_finished += res

    db_queue.join()
    ngrams_executor.shutdown(wait=True)
    db_executor.shutdown(wait=True)
    io_executor.shutdown()

    pbar.close()

    logger.info("Completed {0} items".format(items_finished))
    logger.info("Harvest finished in " + str(time.perf_counter() - time_start) + "s.")

    close_connection(connection)
