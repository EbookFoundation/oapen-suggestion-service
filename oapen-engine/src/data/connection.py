#!/usr/bin/python
import psycopg2
from data.config import config


def get_connection():
    conn = None
    try:
        params = config()

        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        cur = conn.cursor()

        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        db_version = cur.fetchone()
        print(db_version)

        # TODO: Register adapters for suggestion and ngram types

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn
    return conn


def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Database connection closed.")


connection = get_connection()
