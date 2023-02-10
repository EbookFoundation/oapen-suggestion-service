from data.connection import get_connection


def create_schema(connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE SCHEMA oapen_suggestions;

        CREATE TYPE oapen_suggestions.suggestion AS (handle text, similarity float);
        CREATE TYPE oapen_suggestions.ngram AS (ngram text, count int);

        CREATE OR REPLACE FUNCTION update_modtime() 
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW; 
        END;
        $$ language 'plpgsql';

        CREATE TABLE IF NOT EXISTS oapen_suggestions.suggestions (
            handle      text    PRIMARY KEY,
            name		text,
            suggestions	oapen_suggestions.suggestion[],
            created_at  timestamp default current_timestamp,
            updated_at  timestamp default current_timestamp
        );
        CREATE TABLE oapen_suggestions.ngrams (
            handle      text    PRIMARY KEY,
            ngrams      oapen_suggestions.ngram[],
            created_at  timestamp default current_timestamp,
            updated_at  timestamp default current_timestamp
        );

        CREATE TRIGGER update_suggestion_modtime BEFORE UPDATE ON oapen_suggestions.suggestions FOR EACH ROW EXECUTE PROCEDURE update_modtime();
        CREATE TRIGGER update_ngrams_modtime BEFORE UPDATE ON oapen_suggestions.ngrams FOR EACH ROW EXECUTE PROCEDURE update_modtime();
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


def run():
    connection = get_connection()

    drop_schema(connection)
    create_schema(connection)

    connection.close()


def main():
    run()


if __name__ == "__main__":
    main()
