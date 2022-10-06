from sqlite3 import connect
from venv import create
import psycopg2
from data.connection import get_connection
from model.oapen_types import OapenSuggestion, OapenItem, transform_item_data
import data.oapen as OapenAPI
from data.oapen_db import add_many_suggestions



def mock_suggestion_rows(connection, n = 10):
    cursor = connection.cursor()
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