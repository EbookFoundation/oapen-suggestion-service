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

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn
    return conn


if __name__ == "__main__":
    connect()
