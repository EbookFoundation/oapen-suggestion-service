from sqlite3 import connect
from venv import create

import psycopg2

from data.connection import get_connection


def create_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TYPE suggestion AS (id uuid, rank int);
        CREATE SCHEMA oapen_suggestions
            CREATE TABLE IF NOT EXISTS suggestions (
                item_id		uuid	PRIMARY KEY,
                name		text,
                suggestions	suggestion[]
            );
        """
    )

    cursor.close()


def drop_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
        DROP TABLE IF EXISTS suggestions CASCADE;
        DROP TYPE IF EXISTS suggestion CASCADE;
        """
    )

    cursor.close()


connection = get_connection()

drop_schema(connection)
create_schema(connection)

connection.close()
