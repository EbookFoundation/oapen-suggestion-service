import multiprocessing
import queue
from typing import List

import model.ngrams as OapenEngine
from logger.base_logger import logger
from model.oapen_types import OapenItem


def ngrams_task(
    item_queue: multiprocessing.JoinableQueue,
    db_queue: multiprocessing.JoinableQueue,
    event: multiprocessing.Event,
):
    count = 0
    while True:
        try:
            entry = item_queue.get_nowait()

            url: str = entry[0]
            items: List[OapenItem] = entry[1]

            ngrams = OapenEngine.get_ngrams_for_items(items)

            db_queue.put((url, ngrams))

            item_queue.task_done()
        except queue.Empty:
            if event.is_set():
                break
            else:
                continue
        except Exception as e:
            logger.error(e)

    return count
