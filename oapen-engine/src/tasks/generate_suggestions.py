import concurrent.futures
import time
from collections import Counter
from threading import Lock
from typing import List

import config
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from model.oapen_types import Ngram, NgramRow, SuggestionRow
from tqdm.auto import tqdm

# initial seed -> get suggestions on everything n^2
# weekly update ->
# for existing books, get suggestions based on set of new books
# for new books, get suggestions based on all books
# optimization: only suggest once per pair


def truncate_ngrams_list(item: NgramRow) -> List[NgramRow]:
    ngrams = [
        Ngram(ngram=x[0], count=0)
        for x in item.ngrams[0 : min(len(item.ngrams), config.TOP_K_NGRAMS_COUNT)]
    ]
    return item._replace(ngrams=ngrams)


def suggestion_task(items: List[NgramRow], all_items: List[NgramRow], db_mutex, db):
    suggestions: List[SuggestionRow] = []
    for item_a in items:
        for item_b in all_items:
            if item_a.handle == item_b.handle:
                continue

            score = len(list(filter(lambda x: x in item_b.ngrams, item_a.ngrams)))

            if score >= config.SCORE_THRESHOLD:
                suggestions.append(
                    SuggestionRow(
                        handle=item_a.handle,
                        suggestion=item_b.handle,
                        suggestion_name=item_b.name,
                        suggestion_thumbnail=item_b.thumbnail,
                        score=score,
                    )
                )

    if len(suggestions) > 0:
        db_mutex.acquire()
        db.add_many_suggestions(suggestions)
        db_mutex.release()

    return len(items)

def refresh(future, counter, pbar):
    pbar.update(future.result())
    counter["items_updated"] += future.result()
    pbar.refresh()


def run():
    connection = get_connection()
    db = OapenDB(connection)

    all_items: List[NgramRow] = db.get_all_ngrams(get_empty=False)

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=config.SUGGESTIONS_MAX_WORKERS
    )
    futures = []
    db_mutex = Lock()

    counter = Counter(items_updated=0)

    pbar = tqdm(
        total=len(all_items),
        mininterval=0,
        miniters=1,
        leave=True,
        position=0,
        initial=0,
    )

    logger.info("Getting suggestions for {0} items...".format(str(len(all_items))))
    time_start = time.perf_counter()

    # Get only top k ngrams for all items before processing
    for i in range(len(all_items)):
        all_items[i] = truncate_ngrams_list(all_items[i])

    chunks = [
        all_items[i : i + config.SUGGESTIONS_MAX_ITEMS]
        for i in range(0, len(all_items), config.SUGGESTIONS_MAX_ITEMS)
    ]

    for chunk in chunks:
        future = executor.submit(suggestion_task, chunk, all_items, db_mutex, db)
        future.add_done_callback(lambda x: refresh(x, counter, pbar))
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        pass

    logger.info(
        "Updated "
        + str(counter["items_updated"])
        + " suggestions in "
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
