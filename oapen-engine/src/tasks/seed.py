import time
from typing import List

import data.oapen as OapenAPI
import model.ngrams as OapenEngine
from model.oapen_types import OapenItem

COLLECTION_NAME = "Knowledge Unlatched (KU)"
LIMIT = 100
print("Getting items for OapenDB...")
time_start = time.perf_counter()
items: List[OapenItem] = OapenAPI.get_collection_items_by_label(
    "Knowledge Unlatched (KU)", limit=LIMIT
)


print(
    "Found "
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)

time_start = time.perf_counter()
print("Storing ngrams in DB...")
OapenEngine.cache_ngrams_from_items(items)

print(
    "Updated "
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)
