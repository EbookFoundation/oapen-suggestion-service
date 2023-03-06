import errno
import multiprocessing
import time

import data.oapen as OapenAPI
from logger.base_logger import logger

MAX_RETRIES = 3
RETRY_DELAY = 10


def harvest_task(url: str, items: multiprocessing.JoinableQueue) -> int or None:
    ret = 0

    logger.info("(IO) Starting - " + url)
    for i in range(MAX_RETRIES):
        logger.debug("(IO) {}/{} - {}".format(i, MAX_RETRIES, url))
        try:
            collection_items = OapenAPI.get_collection_items_by_endpoint(url)

            if collection_items is not None:
                logger.debug("(IO) DONE - " + " - found " + str(len(collection_items)))

                items.put((url, collection_items))

                ret = len(collection_items)
                break
        except IOError as e:
            if e.errno == errno.EPIPE:
                logger.warning("(IO) (will retry) - " + str(e))
            else:
                logger.error("(IO) (will retry) - " + str(e))
            continue
        except Exception as e:
            logger.error("(IO) (will retry) - " + str(e))

            time.sleep(RETRY_DELAY)

    return ret
