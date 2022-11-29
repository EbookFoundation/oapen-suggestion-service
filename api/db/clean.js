require("dotenv").config({ path: "./config.env" });
const db = require("./connection.js");

db.none(`
DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
DROP TABLE IF EXISTS suggestions CASCADE;
DROP TYPE IF EXISTS suggestion CASCADE;
`);

db.none(`
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
`);
