#!/usr/bin/python
import psycopg2
from data.config import config
from logger.base_logger import logger
from psycopg2.extras import register_composite


def get_connection():
    conn = None
    try:
        params = config()

        logger.info("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        cur = conn.cursor()

        logger.info("Connected to database.")

        cur.close()

        register_composite("oapen_suggestions.suggestion", conn, globally=True)
        register_composite("oapen_suggestions.ngram", conn, globally=True)

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        return conn


def close_connection(conn):
    if conn is not None:
        conn.close()
        logger.info("Database connection closed.")
