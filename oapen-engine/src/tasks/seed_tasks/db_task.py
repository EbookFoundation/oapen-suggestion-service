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
            urls = []
            items = []

            for e in entries:
                urls += e[0]
                items += e[1]

            logger.debug("(DB) - Inserting {0} item(s).".format(len(items)))

            db.add_many_ngrams(items)

            logger.debug("(DB) - Inserted {0} item(s).".format(len(items)))

            for url in urls:
                db.update_url(url, True)

            for _ in range(len(items)):
                db_queue.task_done()

            return len(items)
        except Exception as e:
            logger.error(e)
            return -1

    while not event.is_set():
        if db_queue.qsize() >= ENTRIES_PER_INSERT:
            entries = [db_queue.get() for _ in range(ENTRIES_PER_INSERT)]
            insert_items(entries)

    if not db_queue.empty():
        entries = []
        while not db_queue.empty():
            entries.append(db_queue.get())
        insert_items(entries)

    logger.info("(DB) - Exiting...")
    return
