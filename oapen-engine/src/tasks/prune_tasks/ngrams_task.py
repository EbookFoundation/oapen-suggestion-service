import multiprocessing
import queue

import model.ngrams as OapenEngine
from logger.base_logger import logger


def ngrams_task(
    item_queue: multiprocessing.JoinableQueue,
    db_queue: multiprocessing.JoinableQueue,
    event: multiprocessing.Event,
):
    count = 0
    while True:
        try:
            item = item_queue.get_nowait()

            ngrams = OapenEngine.get_ngrams_for_items([item])

            db_queue.put(ngrams)

            item_queue.task_done()
        except queue.Empty:
            if event.is_set():
                break
            else:
                continue
        except Exception as e:
            logger.error(e)

    return count
