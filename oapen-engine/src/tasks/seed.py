import concurrent.futures
import queue
import time
from threading import Event, Lock, get_ident

import config
import data.oapen as OapenAPI
import data.oapen_db as OapenDB
import model.ngrams as OapenEngine

# threadsafe queue
items: queue.Queue = queue.Queue()

mutex = Lock()


def ngrams_task(items, event):
    global items_consumed

    print(str(get_ident()) + ": Starting consumer thread")

    while True:
        if not items.empty():
            ngrams_items = []

            ngrams_items.append(items.get())

            print(
                str(get_ident())
                + ": Generating ngram for "
                + str(len(ngrams_items))
                + " item."
            )

            ngrams = OapenEngine.get_ngrams_for_items(ngrams_items)

            mutex.acquire()
            try:
                OapenDB.add_many_ngrams(ngrams)
                print(
                    str(get_ident())
                    + ": Generated ngrams for "
                    + str(len(ngrams_items))
                    + " items."
                )
                print("Items remaining: " + str(items.qsize()))

            finally:
                mutex.release()
        elif event.is_set():
            print(str(get_ident()) + ": Killing consumer thread")
            break


def data_task(collection, limit, offset, items):
    global ip_mutex
    print(str(get_ident()) + ": Starting thread for " + collection["name"])

    collection_items = OapenAPI.get_collection_items_by_id(
        collection["uuid"], limit=limit, offset=offset
    )

    for i in collection_items:
        items.put(i)

    print(
        str(get_ident())
        + ": Found "
        + str(len(collection_items))
        + " from collection "
        + collection["name"]
    )

    print("Items remaining: " + str(items.qsize()))


print("Getting items for OapenDB...")
time_start = time.perf_counter()
collections = OapenAPI.get_collections_from_community(OapenAPI.BOOKS_COMMUNITY_ID)

expected_items = len(collections) * config.COLLECTION_IMPORT_LIMIT

event = Event()

producers_done = 0
producer_futures = []
consumer_futures = []
with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
    for collection in collections:
        for offset in range(
            0, config.COLLECTION_IMPORT_LIMIT, config.ITEMS_PER_IMPORT_THREAD
        ):
            future = executor.submit(
                data_task, collection, config.ITEMS_PER_IMPORT_THREAD, offset, items
            )
            producer_futures.append(future)

    for _ in range(0, config.DATA_IMPORT_CONSUMERS):
        future = executor.submit(ngrams_task, items, event)
        consumer_futures.append(future)

    for future in concurrent.futures.as_completed(producer_futures):
        result = future.result()
        producers_done += 1

    for future in concurrent.futures.as_completed(consumer_futures):
        result = future.result()
        if producers_done == len(producer_futures):
            event.set()


print("Finished in " + str(time.perf_counter() - time_start) + "s.")
