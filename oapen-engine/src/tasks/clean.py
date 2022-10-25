from data.connection import get_connection


def create_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE SCHEMA oapen_suggestions;

        CREATE TYPE oapen_suggestions.suggestion AS (handle text, similarity float);
        CREATE TYPE oapen_suggestions.ngram AS (ngram text, count int);

        CREATE TABLE IF NOT EXISTS oapen_suggestions.suggestions (
            handle      text    PRIMARY KEY,
            name		text,
            suggestions	oapen_suggestions.suggestion[]
        );
        CREATE TABLE oapen_suggestions.ngrams (
            handle      text    PRIMARY KEY,
            ngrams      oapen_suggestions.ngram[]
        );
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
        DROP TYPE IF EXISTS oapen_suggestions.suggestion CASCADE;
        DROP TYPE IF EXISTS oapen_suggestions.ngram CASCADE;
        """
    )

    cursor.close()


connection = get_connection()

drop_schema(connection)
create_schema(connection)

connection.close()
