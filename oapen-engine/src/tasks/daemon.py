# Daemon to run processes in the background
import os
import signal
import sys
import time

from clean import run as run_clean
from data.connection import get_connection
from data.oapen_db import OapenDB
from generate_suggestions import run as run_generate_suggestions
from refresh_items import run as run_refresh_items
from seed import run as run_seed


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

print("Daemon up and running")

conn = get_connection()
db = OapenDB(conn)

if int(os.environ["RUN_CLEAN"]) == 1 or (
    not db.table_exists("suggestions") or not db.table_exists("ngrams")
):
    print("STARTED: clean.py")
    run_clean()
    print("STOPPED: clean.py")

conn.close()

print("STARTED: seed.py")
run_seed()
print("STOPPED: seed.py")

run_generate_suggestions()
acc = 0

while True:
    print("Daemon still running")

    if acc >= int(os.environ["REFRESH_PERIOD"]):
        print("STARTED: refresh items")
        run_refresh_items()
        print("STOPPED: refresh items")

        print("STARTED: generate suggestions")
        run_generate_suggestions()
        print("STOPPED: generate suggestions")
        acc = 0

    time.sleep(60)
    acc += 60

print("Daemon down")
