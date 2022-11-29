import concurrent.futures
import time
from threading import Lock, get_ident
from typing import List

import config
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from model.oapen_types import NgramRow, SuggestionRow
from tqdm import tqdm

# for each item in ngrams
#   get suggestions for item
#   store in database

# initial seed -> get suggestions on everything n^2
# weekly update ->
# for existing books, get suggestions based on set of new books
# for new books, get suggestions based on all books
# optimization: only suggest once per pair


def suggestion_task(items, all_items, mutex, suggestions):
    print(
        "Starting thread " + str(get_ident()) + " with " + str(len(items)) + " items."
    )
    for item_a in items:
        handle_a = item_a[0]
        ngrams_a = [
            x[0] for x in item_a[1][0 : min(len(item_a[1]), config.TOP_K_NGRAMS_COUNT)]
        ]

        item_suggestions = []

        for item_b in all_items:
            handle_b = item_b[0]
            ngrams_b = [
                x[0]
                for x in item_b[1][0 : min(len(item_b[1]), config.TOP_K_NGRAMS_COUNT)]
            ]
            if handle_a == handle_b:
                continue

            repeated = len(list(filter(lambda x: x in ngrams_b, ngrams_a)))

            if repeated >= config.SCORE_THRESHOLD:
                item_suggestions.append((handle_b, repeated))

        mutex.acquire()
        item_suggestions.sort(key=lambda x: x[1], reverse=True)
        mutex.release()

        suggestions.append((handle_a, handle_a, item_suggestions))


def main():

    mutex = Lock()
    connection = get_connection()
    db = OapenDB(connection)

    all_items: List[NgramRow] = db.get_all_ngrams()
    suggestions: List[SuggestionRow] = []

    futures = []

    # Get only top k ngrams for all items before processing
    for item in all_items:
        item = (
            item[0],
            [x[0] for x in item[1]][0 : min(len(item[1]), config.TOP_K_NGRAMS_COUNT)],
        )

    time_start = time.perf_counter()

    n = config.SUGGESTIONS_MAX_ITEMS

    chunks = [all_items[i : i + n] for i in range(0, len(all_items), n)]

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=config.SUGGESTIONS_MAX_WORKERS
    ) as executor:

        for chunk in chunks:
            future = executor.submit(
                suggestion_task, chunk, all_items, mutex, suggestions
            )
            futures.append(future)

        with tqdm(total=len(futures)) as pbar:

            for future in concurrent.futures.as_completed(futures):
                future.result()
                pbar.update(1)

    db.add_many_suggestions(suggestions)

    print(
        "Updated suggestions for "
        + str(len(all_items))
        + " items in "
        + str(time.perf_counter() - time_start)
        + "s."
    )

    close_connection(connection)


if __name__ == "__main__":
    main()
