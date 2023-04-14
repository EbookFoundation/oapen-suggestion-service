import itertools
import multiprocessing
from threading import Event

import config
from data.oapen_db import OapenDB
from logger.base_logger import logger

ENTRIES_PER_INSERT = int(config.NGRAMS_PER_INSERT / config.ITEMS_PER_IMPORT_THREAD)


def db_task(db: OapenDB, db_queue: multiprocessing.Queue, event: Event):
    logger.info("(DB) - Starting DB task")

    def insert_items(entries):
        try:

            urls = [e[0] for e in entries]
            items = list(itertools.chain(*[e[1] for e in entries]))

            logger.info("(DB) - Inserting {0} item(s).".format(len(items)))

            db.add_many_ngrams(items)

            logger.info("(DB) - Inserted {0} item(s).".format(len(items)))

            for url in urls:
                db.update_url(url, True)

            return
        except Exception as e:
            logger.error(e)
            return -1

    while not event.is_set():
        if db_queue.qsize() >= ENTRIES_PER_INSERT:
            entries = [db_queue.get() for _ in range(ENTRIES_PER_INSERT)]
            count = len(entries)
            insert_items(entries)
            for _ in range(count):
                db_queue.task_done()

    if not db_queue.empty():
        entries = []
        while not db_queue.empty():
            entries.append(db_queue.get())
        count = len(entries)
        insert_items(entries)
        for _ in range(count):
            db_queue.task_done()

    logger.info("(DB) - Exiting...")
    return
