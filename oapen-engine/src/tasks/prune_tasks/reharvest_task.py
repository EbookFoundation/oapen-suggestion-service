import errno
import multiprocessing
import time

import data.oapen as OapenAPI
from logger.base_logger import logger

MAX_RETRIES = 3
RETRY_DELAY = 10


def reharvest_task(handle: str, items: multiprocessing.JoinableQueue) -> int or None:
    ret = 0
    handle = handle[0]
    logger.info("(IO) Starting - " + str(handle))
    for i in range(MAX_RETRIES):
        logger.debug("(IO) {}/{} - {}".format(i, MAX_RETRIES, handle))
        try:
            item = OapenAPI.get_item(handle)

            if item is not None:
                logger.debug("(IO) DONE")
                items.put(item)
                ret = 1
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
