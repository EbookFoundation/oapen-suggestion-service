from typing import List

import data.oapen as OapenAPI
from data.connection import get_connection
from data.oapen_db import add_many_suggestions
from model.oapen_types import OapenItem


def mock_suggestion_rows(n=10):
    items: List[OapenItem] = OapenAPI.get_collection_items_by_label(
        "Knowledge Unlatched (KU)"
    )

    rows = []
    for i in range(min(10, len(items))):
        rows.append((items[i].handle, items[i].name, [(items[i].handle, i)]))

    return rows


connection = get_connection()

rows = mock_suggestion_rows(connection)
add_many_suggestions(connection, rows)

connection.close()
