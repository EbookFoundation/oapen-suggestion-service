import concurrent.futures
import os
import queue
import signal
import sys
import time
from multiprocessing import Manager, cpu_count, current_process
from threading import Event, get_ident

import config
import data.oapen as OapenAPI
import model.ngrams as OapenEngine
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB

# from util.kill_processes import kill_child_processes


def data_task(collection, limit, offset, items):
    print(str((get_ident())) + ": START - " + collection["name"])

    ret = 0

    try:
        collection_items = OapenAPI.get_collection_items_by_id(
            collection["uuid"], limit=limit, offset=offset
        )

        print(
            str((get_ident()))
            + ": (IO) DONE - "
            + collection["name"]
            + " - found "
            + str(len(collection_items))
        )

        for x in collection_items:
            items.put(x)

        ret = len(collection_items)
    except Exception as e:
        print(str(get_ident()) + ": (IO) ERROR - " + collection["name"])
        print(e)

    print(str(get_ident()) + " (IO): Exiting...")
    return ret


def ngrams_task(item_queue, db_queue, event):
    while True:
        if item_queue.empty() and event.is_set():
            break

        try:
            items = [item_queue.get_nowait()]

            ngrams = OapenEngine.get_ngrams_for_items(items)

            for x in ngrams:
                db_queue.put(x)

            item_queue.task_done()
        except queue.Empty:
            if event.is_set():
                break
            else:
                continue
    print(str(get_ident()) + " (NGRAMS): Exiting...", flush=True)


def db_task(db, db_queue, event: Event):
    def insert_items(items):
        try:
            print(
                "{0} (DB): Inserting {1} items.".format(
                    str(current_process().ident), len(items)
                ),
                flush=True,
            )
            db.add_many_ngrams(items)
            print(
                "{0} (DB): Inserted {1} items.".format(
                    str(current_process().ident), len(items)
                ),
                flush=True,
            )
        except Exception as e:
            print(e)
        return

    while not event.is_set():
        if db_queue.full():
            items = [db_queue.get() for _ in range(config.NGRAMS_PER_INSERT)]
            insert_items(items)

    print("(DB) Exiting loop")

    if not db_queue.empty():
        items = []
        while not db_queue.empty():
            items.append(db_queue.get())
        print("Final insert")
        insert_items(items)

    print(str(current_process().ident) + " (DB): Exiting...", flush=True)

    return


def run():
    connection = get_connection()
    manager = Manager()
    db_manager = Manager()
    db = OapenDB(connection)

    item_queue: queue.Queue() = manager.Queue()
    db_queue: queue.Queue() = db_manager.Queue(config.NGRAMS_PER_INSERT)

    ngrams_event = manager.Event()
    db_event = manager.Event()

    items_produced = 0
    producers_done = 0
    consumers_done = 0
    producer_futures = []
    consumer_futures = []
    db_futures = []
    total_items = 0

    io_pool = concurrent.futures.ThreadPoolExecutor(max_workers=config.IO_MAX_WORKERS)
    ngrams_pool = concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count())
    db_pool = concurrent.futures.ThreadPoolExecutor()

    def shutdown():
        print("Stopping import.")
        db_pool.shutdown(wait=False, cancel_futures=True)
        io_pool.shutdown(wait=False, cancel_futures=True)
        ngrams_pool.shutdown(wait=False, cancel_futures=True)
        close_connection(connection)

    def signal_handler(signal, frame):
        print("\nprogram exiting gracefully")
        shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    def print_progress():
        print(
            "Producers done: {0}/{1}\t\tItems imported: {2}/{3}".format(
                str(producers_done),
                str(len(producer_futures)),
                str(items_produced),
                str(total_items),
            )
        )

    print(str(os.getpid()) + ": Getting items for OapenDB...")
    time_start = time.perf_counter()
    collections = OapenAPI.get_all_collections()

    #
    # Ngrams generation: Using multiprocessing, generate trigrams for each item that was imported.
    #
    for _ in range(cpu_count()):
        consumer_futures.append(
            ngrams_pool.submit(ngrams_task, item_queue, db_queue, ngrams_event)
        )

    db_futures.append(db_pool.submit(db_task, db, db_queue, db_event))

    #
    #  Data import: COLLECTION_IMPORT_LIMIT items from all collections in the OAPEN catalog
    #

    url_params = []
    COLLECTION_IMPORT_LIMIT = int(os.environ["COLLECTION_IMPORT_LIMIT"])

    for collection in collections:
        num_items = (
            collection["numberItems"]
            if COLLECTION_IMPORT_LIMIT == 0
            else min(COLLECTION_IMPORT_LIMIT, collection["numberItems"])
        )

        total_items += num_items

        for offset in range(0, num_items, config.ITEMS_PER_IMPORT_THREAD):
            url_params += [(collection, config.ITEMS_PER_IMPORT_THREAD, offset)]

    for url in url_params:
        producer_futures.append(
            io_pool.submit(data_task, url[0], url[1], url[2], item_queue)
        )
        time.sleep(1)

    for future in concurrent.futures.as_completed(producer_futures):
        result = future.result()

        # Something went wrong during import, most likely a rate limiting error. Shut down and try again.
        # if result == -1:
        #     shutdown()
        # return

        items_produced += result
        producers_done += 1

        print_progress()

    io_pool.shutdown(wait=True)

    if (producers_done == len(producer_futures)) or io_pool._shutdown:
        ngrams_event.set()
        print("Set ngrams event.")
        item_queue.join()
        print("Joined item_queue.")
        db_event.set()
        print("Set db_event.")

    for future in concurrent.futures.as_completed(consumer_futures):
        consumers_done += 1

        print_progress()

    # DB population: Populate the database with ngrams for each OAPEN item

    for future in concurrent.futures.as_completed(db_futures):
        print_progress()

    ngrams_pool.shutdown(wait=True)
    db_pool.shutdown(wait=True)

    print(
        "Ngrams: {0}\t\tSuggestions: {1}".format(
            db.count_ngrams(), db.count_suggestions()
        )
    )
    print("Finished in " + str(time.perf_counter() - time_start) + "s.")
    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
