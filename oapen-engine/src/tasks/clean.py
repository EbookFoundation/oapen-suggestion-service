import os
import sys

import config
import data.oapen as OapenAPI
from data.connection import get_connection
from data.oapen_db import OapenDB
from logger.base_logger import logger


def create_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE SCHEMA oapen_suggestions;

        CREATE TYPE oapen_suggestions.ngram AS (ngram text, count int);

        CREATE OR REPLACE FUNCTION update_modtime() 
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW; 
        END;
        $$ language 'plpgsql';

        CREATE TABLE IF NOT EXISTS oapen_suggestions.suggestions (
            handle      text,
            name		text,
            suggestion	text,
            score       int,
            created_at  timestamp default current_timestamp,
            updated_at  timestamp default current_timestamp,
            PRIMARY KEY (handle, suggestion)
        );

        CREATE TABLE IF NOT EXISTS oapen_suggestions.ngrams (
            handle      text    PRIMARY KEY,
            ngrams      oapen_suggestions.ngram[],
            created_at  timestamp default current_timestamp,
            updated_at  timestamp default current_timestamp
        );

        CREATE TABLE IF NOT EXISTS oapen_suggestions.endpoints (
            endpoint    text        PRIMARY KEY,
            completed   boolean     DEFAULT FALSE,
            updated_at  timestamp default current_timestamp
        );

        CREATE TRIGGER update_suggestion_modtime BEFORE UPDATE ON oapen_suggestions.suggestions FOR EACH ROW EXECUTE PROCEDURE update_modtime();
        CREATE TRIGGER update_ngrams_modtime BEFORE UPDATE ON oapen_suggestions.ngrams FOR EACH ROW EXECUTE PROCEDURE update_modtime();
        CREATE TRIGGER update_endpoint_modtime BEFORE UPDATE ON oapen_suggestions.endpoints FOR EACH ROW EXECUTE PROCEDURE update_modtime();

        CREATE INDEX idx_suggestion
        ON oapen_suggestions.suggestions(handle, suggestion);

        ALTER TABLE oapen_suggestions.suggestions
            ADD CONSTRAINT uq_Suggestion UNIQUE(handle, suggestion);
        """
    )

    cursor.close()


def drop_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.suggestions CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.ngrams CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.endpoints CASCADE;
        DROP TYPE IF EXISTS oapen_suggestions.ngram CASCADE;
        """
    )

    cursor.close()


def seed_endpoints(connection):

    collections = OapenAPI.get_all_collections()

    if collections is None:
        logger.error("Could not fetch collections from OAPEN server. Is it down?")
        sys.exit(1)

    db = OapenDB(connection)

    endpoints = []

    COLLECTION_IMPORT_LIMIT = int(os.environ["COLLECTION_IMPORT_LIMIT"])

    for collection in collections:
        num_items = (
            collection["numberItems"]
            if COLLECTION_IMPORT_LIMIT == 0
            else min(COLLECTION_IMPORT_LIMIT, collection["numberItems"])
        )

        for offset in range(0, num_items, config.ITEMS_PER_IMPORT_THREAD):
            x = "/rest/collections/{id}/items?limit={limit}&offset={offset}&expand=bitstreams,metadata".format(
                id=collection["uuid"],
                limit=config.ITEMS_PER_IMPORT_THREAD,
                offset=offset,
            )
            endpoints.append(x)

    db.add_urls(endpoints)


def run():
    connection = get_connection()

    drop_schema(connection)
    create_schema(connection)
    seed_endpoints(connection)

    connection.close()
