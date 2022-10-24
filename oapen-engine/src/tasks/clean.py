from data.connection import get_connection


def create_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TYPE suggestion AS (handle text, rank int);
        CREATE SCHEMA oapen_suggestions
            CREATE TABLE IF NOT EXISTS oapen_suggestions.suggestions (
                handle      text    PRIMARY KEY,
                name		text,
                suggestions	suggestion[]
            );
            CREATE TABLE oapen_suggestions.ngrams (
                handle      text    PRIMARY KEY,
                ngrams      text[]
            );
        """
    )

    cursor.close()


def drop_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
        DROP TABLE IF EXISTS suggestions CASCADE;
        DROP TABLE IF EXISTS ngrams CASCADE;
        DROP TYPE IF EXISTS suggestion CASCADE;
        """
    )

    cursor.close()


connection = get_connection()

drop_schema(connection)
create_schema(connection)

connection.close()
