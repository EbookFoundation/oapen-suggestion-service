import concurrent.futures
import time
from threading import Lock
from typing import List

import config
import tqdm
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from model.oapen_types import NgramRow, SuggestionRow
from model.stopwords import get_all_stopwords


def suggestion_task(items, all_items, mutex, suggestions):
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


def run():
    connection = get_connection()
    db = OapenDB(connection)

    all_stopwords = get_all_stopwords()
    print(all_stopwords)
    refresh_handles = []

    # Get the list of (only) the new stopwords
    logger.info("Searching existing items for added stopwords")
    new_stopwords = list(db.get_new_stopwords(all_stopwords))

    # Update the stopwords in the database
    # (used to determine which are new next run)
    db.update_stopwords(all_stopwords)

    if new_stopwords == None:
        logger.info("No new stopwords! Aborting suggestion re-run")
    else:
        logger.info("Added new stopwords: " + ", ".join(new_stopwords))

        # Get the handles of all items with ngrams containing the new stopwords
        refresh_handles = db.get_all_items_containing_stopwords(new_stopwords)

        # Rerun generate_suggestions on the flagged items
        refresh_items: List[NgramRow] = db.get_ngrams_with_handles(refresh_handles)
        refreshed_suggestions: List[SuggestionRow] = []

        # Remove empty entries
        refresh_items = [item for item in refresh_items if len(item[1]) != 0]

        logger.info(
            "Regenerating suggestions for {0} items".format(len(refresh_handles))
        )

        # Get only top k ngrams for all items before processing
        for item in refresh_items:
            item = (
                item[0],
                [x[0] for x in itme[1]][
                    0 : min(len(item[1]), config.TOP_K_NGRAMS_COUNT)
                ],
            )

        time_start = time.perf_counter()
        n = config.SUGGESTIONS_MAX_ITEMS

        chunks = [refresh_items[i : i + n] for i in range(0, len(refresh_items), n)]

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=config.SUGGESTIONS_MAX_WORKERS
        ) as executor:

            for chunk in chunks:
                future = executor.submit(
                    suggestion_task, chunk, refresh_items, mutex, refreshed_suggestions
                )
                futures.append(future)

            with tqdm.tqdm(
                total=len(futures),
                mininterval=0,
                miniters=1,
                leave=True,
                position=0,
                initial=0,
            ) as pbar:

                for future in concurrent.futures.as_completed(futures):
                    future.result()
                    pbar.update(1)

        db.add_many_suggestions(refreshed_suggestions)

        logger.info(
            "Updated suggestions for "
            + str(len(refresh_items))
            + " items in "
            + str(time.perf_counter() - time_start)
            + "s."
        )

    # Close the database connection
    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
