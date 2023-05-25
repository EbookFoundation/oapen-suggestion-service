import os
import sys

from tasks import config
import data.oapen as OapenAPI
from data.connection import get_connection
from data.oapen_db import OapenDB
from data.oapen_oai import get_oapen_handles
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
    logger.warning("WARNING: DROPPING DATABASE!")
    cursor = connection.cursor()
    cursor.execute(
        """
        DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.suggestions CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.ngrams CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.endpoints CASCADE;
        DROP TABLE IF EXISTS oapen_suggestions.migrate;
        DROP TYPE IF EXISTS oapen_suggestions.ngram CASCADE;
        """
    )

    cursor.close()


def get_endpoints():
    for handle, item_type in get_oapen_handles():
        yield OapenAPI.GET_STREAM_QUERY.format(handle=handle)


def seed_endpoints(connection):
    db = OapenDB(connection)
    endpoints = get_endpoints()
    db.add_urls(endpoints)


def mark_for_cleaning(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE SCHEMA IF NOT EXISTS oapen_suggestions;
        CREATE TABLE IF NOT EXISTS oapen_suggestions.migrate (migrate boolean);
        """
    )
    cursor.close()

def mark_no_clean(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE SCHEMA IF NOT EXISTS oapen_suggestions;
        DROP TABLE IF EXISTS oapen_suggestions.migrate;
        """
    )
    cursor.close()

def run():
    connection = get_connection()

    drop_schema(connection)
    create_schema(connection)
    mark_no_clean(connection)
    #seed_endpoints(connection)

    connection.close()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ["now", "true", "false"]:
        if sys.argv[1] == "now":
            run()
        elif sys.argv[1] == "true":
            connection = get_connection()
            mark_for_cleaning(connection)
            logger.warning("WARNING: The database will be ERASED on the next run.")
            connection.close()
        elif sys.argv[1] == "false":
            connection = get_connection()
            mark_no_clean(connection)
            logger.info("The database will not be cleaned on the next run.")
            connection.close()
    else:
        logger.error("Invalid argument supplied to clean.py. Valid options are 'now', 'true', or 'false'.")