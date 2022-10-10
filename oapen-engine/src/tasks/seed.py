from sqlite3 import connect
from venv import create

import psycopg2

import data.oapen as OapenAPI
from data.connection import get_connection
from data.oapen_db import add_many_suggestions
from model.oapen_types import OapenItem, OapenSuggestion, transform_item_data


def mock_suggestion_rows(n=10):
    items = OapenAPI.get_items_from_collection("5f664493-8fee-465a-9c22-7ea8e0595775")

    rows = []
    for i in range(min(10, len(items))):
        item = transform_item_data(OapenAPI.get_item(items[i]))
        rows.append((items[i], item.name, [(items[i], i)]))

    return rows


connection = get_connection()

rows = mock_suggestion_rows(connection)
add_many_suggestions(connection, rows)

connection.close()
