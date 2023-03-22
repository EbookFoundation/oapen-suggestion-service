import datetime
import time
from typing import List

import config
import data.oapen as OapenAPI
import model.ngrams as OapenEngine
from data.connection import close_connection, get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger
from model.oapen_types import OapenItem


def run():
    connection = get_connection()
    db = OapenDB(connection)

    logger.debug("Getting items for OapenDB...")
    time_start = time.perf_counter()

    items: List[OapenItem] = OapenAPI.get_updated_items(
        limit=config.REFRESH_IMPORT_LIMIT,
        date=datetime.datetime.now() - datetime.timedelta(config.UPDATE_DAYS_BEFORE),
    )

    logger.debug(
        "Found "
        + str(len(items))
        + " items in "
        + str(time.perf_counter() - time_start)
        + "s."
    )

    time_start = time.perf_counter()
    logger.debug("Storing ngrams in DB...")

    ngrams = OapenEngine.get_ngrams_for_items(items)

    db.add_many_ngrams(ngrams)

    logger.info(
        "Updated "
        + str(len(items))
        + " items in "
        + str(time.perf_counter() - time_start)
        + "s."
    )

    close_connection(connection)


def main():
    run()


if __name__ == "__main__":
    main()
