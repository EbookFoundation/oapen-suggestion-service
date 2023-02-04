import concurrent.futures
import os
import queue
import time
from multiprocessing import Manager, cpu_count
from threading import get_ident

import config
import data.oapen as OapenAPI
import model.ngrams as OapenEngine
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB

# from util.kill_processes import kill_child_processes


def ngrams_task(items):
    print(
        str(get_ident()) + ": Generating ngrams for " + str(len(items)) + " items.",
        flush=True,
    )

    ngrams = OapenEngine.get_ngrams_for_items(items)

    print(
        str(get_ident())
        + ": DONE generating ngrams for "
        + str(len(ngrams))
        + " items.",
        flush=True,
    )

    return ngrams


def data_task(collection, limit, offset, items):
    print(str(get_ident()) + ": Starting thread for " + collection["name"])

    try:
        collection_items = OapenAPI.get_collection_items_by_id(
            collection["uuid"], limit=limit, offset=offset
        )

        print(
            str(get_ident())
            + ": Got "
            + str(len(collection_items))
            + " from collection "
            + collection["name"]
        )

        for x in collection_items:
            items.put(x)

        return len(collection_items)
    except Exception as e:
        print(
            str(get_ident()) + ": Error while getting items from " + collection["name"]
        )
        print(e)
        return -1


def db_task(db, items, lock):
    with lock:
        try:
            print("Inserting {0} items.".format(len(items)))
            db.add_many_ngrams(items)
            print("Inserted {0} items.".format(len(items)))
            return len(items)
        except Exception as e:
            print(e)
            return 0


def run():
    print(str(os.getpid()) + ": Getting items for OapenDB...")
    time_start = time.perf_counter()
    collections = OapenAPI.get_all_collections()

    items: queue.Queue() = queue.Queue()
    db_queue: queue.Queue() = queue.Queue()

    connection = get_connection()
    db = OapenDB(connection)
    manager = Manager()
    lock = manager.Lock()

    items_produced = 0
    items_consumed = 0
    producers_done = 0
    consumers_done = 0
    producer_futures = []
    consumer_futures = []
    db_futures = []

    db_pool = concurrent.futures.ThreadPoolExecutor()
    io_pool = concurrent.futures.ThreadPoolExecutor(max_workers=config.IO_MAX_WORKERS)
    ngrams_pool = concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count())

    def shutdown():
        print("Stopping import.")
        db_pool.shutdown(wait=False)
        io_pool.shutdown(wait=False)
        ngrams_pool.shutdown(wait=False)
        # kill_child_processes(os.getpid())
        close_connection(connection)

    for collection in collections:
        num_items = (
            collection["numberItems"]
            if config.COLLECTION_IMPORT_LIMIT is None
            else config.COLLECTION_IMPORT_LIMIT
        )
        for offset in range(0, num_items, config.ITEMS_PER_IMPORT_THREAD):
            producer_futures.append(
                io_pool.submit(
                    data_task, collection, config.ITEMS_PER_IMPORT_THREAD, offset, items
                )
            )

    for future in concurrent.futures.as_completed(producer_futures):
        result = future.result()

        if result == -1:
            shutdown()
            return

        items_produced += result
        producers_done += 1
        if items.qsize() >= config.NGRAMS_PER_PROCESS:
            ngrams_items = [
                items.get()
                for _ in range(min(config.NGRAMS_PER_PROCESS, items.qsize()))
            ]
            consumer_futures.append(ngrams_pool.submit(ngrams_task, ngrams_items))

        print(
            "Producers done: {0}/{1}\t\tItems imported: {2}\t\tConsumers done: {3}/{4}\t\tItems completed: {5}".format(
                str(producers_done),
                str(len(producer_futures)),
                str(items_produced),
                str(consumers_done),
                str(len(consumer_futures)),
                str(items_consumed),
            )
        )

    io_pool.shutdown(wait=True)

    while not items.empty():
        ngrams_items = [
            items.get() for _ in range(min(items.qsize(), config.NGRAMS_PER_PROCESS))
        ]
        consumer_futures.append(ngrams_pool.submit(ngrams_task, ngrams_items))

    for future in concurrent.futures.as_completed(consumer_futures):
        result = future.result()
        items_consumed += len(result)
        consumers_done += 1

        for res in result:
            db_queue.put(res)

        if db_queue.qsize() >= config.NGRAMS_PER_INSERT:
            items = [db_queue.get() for _ in range(config.NGRAMS_PER_INSERT)]
            db_futures.append(db_pool.submit(db_task, db, items, lock))

        print(
            "Producers done: {0}/{1}\t\tItems imported: {2}\t\tConsumers done: {3}/{4}\t\tItems completed: {5}".format(
                str(producers_done),
                str(len(producer_futures)),
                str(items_produced),
                str(consumers_done),
                str(len(consumer_futures)),
                str(items_consumed),
            )
        )

    ngrams_pool.shutdown(wait=True)

    while not db_queue.empty():
        items = [
            db_queue.get()
            for _ in range(min(config.NGRAMS_PER_INSERT, db_queue.qsize()))
        ]
        db_futures.append(db_pool.submit(db_task, db, items, lock))

    items_stored = 0

    for future in concurrent.futures.as_completed(db_futures):
        res = future.result()
        items_stored += res
        print("Items stored: {0}".format(items_stored))

    db_pool.shutdown(wait=True)

    print("Finished in " + str(time.perf_counter() - time_start) + "s.")
    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
