import concurrent.futures
import time
from collections import Counter
from threading import Lock
from typing import List

import config
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from model.oapen_types import NgramRow, SuggestionRow
from tqdm.auto import tqdm

# initial seed -> get suggestions on everything n^2
# weekly update ->
# for existing books, get suggestions based on set of new books
# for new books, get suggestions based on all books
# optimization: only suggest once per pair


def get_ngrams_list(arr: List[NgramRow]):
    return [x[0] for x in arr[1][0 : min(len(arr[1]), config.TOP_K_NGRAMS_COUNT)]]


def suggestion_task(items, all_items, db_mutex, db):
    suggestions: List[SuggestionRow] = []
    for item_a in items:
        item_suggestions = []

        handle_a = item_a[0]

        for item_b in all_items:
            handle_b = item_b[0]

            if handle_a == handle_b:
                continue

            ngrams_shared = len(list(filter(lambda x: x in item_b[1], item_a[1])))

            if ngrams_shared >= config.SCORE_THRESHOLD:
                item_suggestions.append((handle_b, ngrams_shared))

        item_suggestions.sort(key=lambda x: x[1], reverse=True)
        suggestions.append((handle_a, handle_a, item_suggestions))

    count = len(suggestions)

    db_mutex.acquire()
    db.add_many_suggestions(suggestions)
    db_mutex.release()

    return count


def run():
    db_mutex = Lock()
    connection = get_connection()
    db = OapenDB(connection)

    all_items: List[NgramRow] = db.get_all_ngrams(get_empty=False)

    logger.info("Getting suggestions for {0} items...".format(str(len(all_items))))

    futures = []

    # Get only top k ngrams for all items before processing
    for item in all_items:
        ngrams = get_ngrams_list(item)
        item = (item[0], ngrams)

    time_start = time.perf_counter()

    n = config.SUGGESTIONS_MAX_ITEMS

    chunks = [all_items[i : i + n] for i in range(0, len(all_items), n)]

    counter = Counter(items_updated=0)

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=config.SUGGESTIONS_MAX_WORKERS
    )

    def refresh(future, counter, pbar):
        pbar.update(future.result())
        counter["items_updated"] += future.result()
        pbar.refresh()

    pbar = tqdm(
        total=len(all_items),
        mininterval=0,
        miniters=1,
        leave=True,
        position=0,
        initial=0,
    )

    for chunk in chunks:
        future = executor.submit(suggestion_task, chunk, all_items, db_mutex, db)
        future.add_done_callback(lambda x: refresh(x, counter, pbar))
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        pass

    logger.info(
        "Updated suggestions for "
        + str(counter["items_updated"])
        + " items in "
        + str(time.perf_counter() - time_start)
        + "s."
    )

    executor.shutdown(wait=True)

    pbar.close()
    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
