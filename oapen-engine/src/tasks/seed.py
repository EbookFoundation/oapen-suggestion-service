import time
from threading import Lock, Thread, get_ident
from typing import List

import config
import data.oapen as OapenAPI
import data.oapen_db as OapenDB
import model.ngrams as OapenEngine
from model.oapen_types import OapenItem

mutex = Lock()


def ngrams_task(items):
    print("Starting thread " + str(get_ident) + " with " + str(len(items)) + " items.")
    ngrams = OapenEngine.get_ngrams_for_items(items)
    mutex.acquire()
    try:
        OapenDB.add_many_ngrams(ngrams)
    finally:
        mutex.release()


print("Getting items for OapenDB...")
time_start = time.perf_counter()

items: List[OapenItem] = []
collections = OapenAPI.get_collections_from_community(OapenAPI.BOOKS_COMMUNITY_ID)
for collection in collections:
    collection_items = OapenAPI.get_collection_items_by_id(
        collection["uuid"], limit=int(config.ITEM_IMPORT_LIMIT / len(collections))
    )
    print(
        "Found " + str(len(collection_items)) + " from collection " + collection["name"]
    )
    items += collection_items

print(
    "Found "
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)

time_start = time.perf_counter()
print("Storing ngrams in DB...")
chunks = [
    items[i : i + config.SUGGESTION_BATCH_SIZE]
    for i in range(0, len(items), config.SUGGESTION_BATCH_SIZE)
]
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
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)
