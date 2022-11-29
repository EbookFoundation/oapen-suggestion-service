#!/usr/bin/python
import psycopg2
from data.config import config
from psycopg2.extras import register_composite


def get_connection():
    conn = None
    try:
        params = config()

        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        cur = conn.cursor()

        print("Connected to database.")

        cur.close()

        register_composite("oapen_suggestions.suggestion", conn, globally=True)
        register_composite("oapen_suggestions.ngram", conn, globally=True)

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn


def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Database connection closed.")
