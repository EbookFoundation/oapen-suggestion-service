from typing import List

import data.oapen as OapenAPI
from data.connection import close_connection, connection
from data.oapen_db import add_many_suggestions
from model.oapen_types import OapenItem, SuggestionRow


def mock_suggestion_rows(n=10):
    items: List[OapenItem] = OapenAPI.get_collection_items_by_label(
        "Knowledge Unlatched (KU)"
    )

    rows: List[SuggestionRow] = []
    for i in range(min(n, len(items))):
        rows.append((items[i].handle, items[i].name, []))

    return rows


rows = mock_suggestion_rows(30)
add_many_suggestions(rows)

close_connection(connection)
