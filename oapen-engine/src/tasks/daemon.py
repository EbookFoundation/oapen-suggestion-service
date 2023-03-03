# Daemon to run processes in the background
import os
import signal
import sys
import time

from clean import run as run_clean
from data.connection import get_connection
from data.oapen_db import OapenDB
from generate_suggestions import run as run_generate_suggestions
from logger.base_logger import logger
from refresh_items import run as run_refresh_items
from seed import run as run_seed


def harvest():
    run_seed()
    run_generate_suggestions()


def refresh():
    run_refresh_items()
    run_generate_suggestions()


logger.info("Daemon up")

conn = get_connection()
db = OapenDB(conn)


def signal_handler(signal, frame):
    conn.close()
    logger.info("Daemon exiting.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if int(os.environ["RUN_CLEAN"]) == 1 or (
    not db.table_exists("suggestions") or not db.table_exists("ngrams")
):
    run_clean()

harvest()

harvest_acc = 0
refresh_acc = 0

while True:
    if harvest_acc >= 180:
        urls = db.get_incomplete_urls()
        if len(urls) > 0:
            harvest()
        harvest_acc = 0

    if refresh_acc >= int(os.environ["REFRESH_PERIOD"]):
        refresh()
        refresh_acc = 0

    time.sleep(60)
    refresh_acc += 60
    harvest_acc += 60

logger.info("Daemon down")
