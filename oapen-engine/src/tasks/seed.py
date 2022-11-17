import math
import time
from threading import Lock, Thread, get_ident
from typing import List

import config
import data.oapen as OapenAPI
import data.oapen_db as OapenDB
import model.ngrams as OapenEngine
from model.oapen_types import OapenItem

all_items: List[OapenItem] = []

mutex = Lock()
items_mutex = Lock()


def ngrams_task(items):
    print(
        "Starting thread " + str(get_ident()) + " with " + str(len(items)) + " items."
    )
    ngrams = OapenEngine.get_ngrams_for_items(items)
    mutex.acquire()
    try:
        OapenDB.add_many_ngrams(ngrams)
    finally:
        mutex.release()


def data_task(collection, items):
    print("Starting thread " + str(get_ident()) + " for " + collection["name"])

    collection_items = OapenAPI.get_collection_items_by_id(
        collection["uuid"], limit=int(config.ITEM_IMPORT_LIMIT)
    )

    items_mutex.acquire()
    items += collection_items
    items_mutex.release()
    print(
        "Found " + str(len(collection_items)) + " from collection " + collection["name"]
    )


print("Getting items for OapenDB...")
time_start = time.perf_counter()
collections = OapenAPI.get_collections_from_community(OapenAPI.BOOKS_COMMUNITY_ID)

threads = []

for collection in collections:
    thread = Thread(target=data_task, args=(collection, all_items))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


print(
    "Found "
    + str(len(all_items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)


time_start = time.perf_counter()
print("Storing ngrams in DB...")

n = math.ceil(len(all_items) / config.NGRAMS_THREAD_COUNT)

chunks = [all_items[i : i + n] for i in range(0, len(all_items), n)]
threads = []

for chunk in chunks:
    thread = Thread(target=ngrams_task, args=(chunk,))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(
    "Updated "
    + str(len(all_items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)
