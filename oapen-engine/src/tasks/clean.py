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
            handle                  text,
            suggestion	            text,
            suggestion_name		    text,
            suggestion_thumbnail    text,
            score                   int,
            created_at              timestamp default current_timestamp,
            updated_at              timestamp default current_timestamp,
            PRIMARY KEY (handle, suggestion)
        );

        CREATE TABLE IF NOT EXISTS oapen_suggestions.ngrams (
            handle      text    PRIMARY KEY,
            name        text,
            thumbnail   text,
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


def get_endpoints():
    collections = OapenAPI.get_all_collections()

    if collections is None:
        logger.error("Could not fetch collections from OAPEN server. Is it down?")
        sys.exit(1)

    endpoints = []

    COLLECTION_IMPORT_LIMIT = int(os.environ["COLLECTION_IMPORT_LIMIT"])

    SKIPPED_COLLECTIONS = [
        "1f7c8abd-677e-4275-8b4e-3d8da49f7b36",
        "93223e33-3c7c-47bd-9356-a7878b2814a0",
    ]

    for collection in collections:
        if collection["uuid"] in SKIPPED_COLLECTIONS:
            continue

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

    return endpoints


def seed_endpoints(connection):
    db = OapenDB(connection)
    endpoints = get_endpoints()
    db.add_urls(endpoints)


def run():
    connection = get_connection()

    drop_schema(connection)
    create_schema(connection)
    seed_endpoints(connection)

    connection.close()
