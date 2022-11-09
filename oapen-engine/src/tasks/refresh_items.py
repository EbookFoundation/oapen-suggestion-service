import time
from typing import List

import data.oapen as OapenAPI
import model.ngrams as OapenEngine
from model.oapen_types import OapenItem

print("Refreshing items for OapenDB...")
time_start = time.perf_counter()
items: List[OapenItem] = OapenAPI.get_weekly_items()

print(
    "Found "
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)

print("Storing ngrams in DB...")
OapenEngine.cache_ngrams_from_items(items)

print("Refresh done.")