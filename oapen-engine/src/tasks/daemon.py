# Daemon to run processes in the background
import os
import signal
import sys
import time

import schedule
from clean import run as run_clean
from clean import seed_endpoints
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from generate_suggestions import run as run_generate_suggestions
from logger.base_logger import logger
from refresh_items import run as run_refresh_items
from seed import run as run_seed

conn = get_connection()
db = OapenDB(conn)


def harvest():
    conn = get_connection()
    db = OapenDB(conn)
    seed_endpoints(conn)
    urls = db.get_incomplete_urls()

    close_connection(conn)

    if len(urls) > 0:
        run_seed()
        run_generate_suggestions()


def refresh():
    run_refresh_items()
    run_generate_suggestions()


def main():
    def signal_handler(signal, frame):
        logger.info("Daemon exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    logger.info("Daemon up")

    if db.table_exists("migrate") or not (
        db.table_exists("suggestions")
        and db.table_exists("ngrams")
        and db.table_exists("endpoints")
        and db.type_exists("ngram")
    ):
        run_clean()

    harvest()

    schedule.every().day.at("20:00").do(refresh)
    schedule.every().sunday.at("22:00").do(harvest)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
