require("dotenv").config({ path: "./db/database.env" });
const db = require("./connection.js");

db.none(`
DROP SCHEMA IF EXISTS oapen_suggestions CASCADE;
DROP TABLE IF EXISTS suggestions CASCADE;
DROP TYPE IF EXISTS suggestion CASCADE;
`);

db.none(`
CREATE TYPE suggestion AS (id uuid, rank int);
CREATE SCHEMA oapen_suggestions
    CREATE TABLE IF NOT EXISTS suggestions (
        item_id		uuid	PRIMARY KEY,
        name		text,
        suggestions	suggestion[]
    );`);
