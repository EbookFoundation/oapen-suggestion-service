import time
from typing import List

import data.oapen_db as OapenDB
from data.connection import close_connection, connection
from model.oapen_types import NgramRow, SuggestionRow

# for each item in ngrams
#   get suggestions for item
#   store in database

# initial seed -> get suggestions on everything n^2
# weekly update ->
# for existing books, get suggestions based on set of new books
# for new books, get suggestions based on all books
# optimization: only suggest once per pair


items: List[NgramRow] = OapenDB.get_all_ngrams()

suggestions: List[SuggestionRow] = []

seen_pairs = set()

n_ngrams = 30
score_threshold = 5

time_start = time.perf_counter()
for item_a in items:
    handle_a = item_a[0]
    ngrams_a = [x[0] for x in item_a[1]][0 : min(len(item_a[1]), n_ngrams)]

    item_suggestions = []

    for item_b in items:
        handle_b = item_b[0]
        ngrams_b = [x[0] for x in item_b[1]][0 : min(len(item_b[1]), n_ngrams)]
        if handle_a == handle_b:
            continue

        repeated = len(list(filter(lambda x: x in ngrams_b, ngrams_a)))

        if repeated >= score_threshold:
            item_suggestions.append((handle_b, repeated))

    item_suggestions.sort(key=lambda x: x[1], reverse=True)

    suggestions.append((handle_a, handle_a, item_suggestions))

OapenDB.add_many_suggestions(suggestions)

print(
    "Updated suggestions for "
    + str(len(items))
    + " items in "
    + str(time.perf_counter() - time_start)
    + "s."
)

close_connection(connection)
