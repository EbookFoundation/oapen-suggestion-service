const options = {};
const pgp = require("pg-promise")(options);

class DatabaseConnectionError extends Error {
  constructor(message) {
    super(message);
  }
}

if (
  !(
    process.env.POSTGRES_USERNAME &&
    process.env.POSTGRES_PASSWORD &&
    process.env.POSTGRES_HOST &&
    process.env.POSTGRES_PORT &&
    process.env.POSTGRES_DB_NAME
  )
)
  throw new DatabaseConnectionError(
    "Some Postgres environment variables weren't found. Please set them in the .env file."
  );

const connection_string = `postgresql://${process.env.POSTGRES_USERNAME}:${process.env.POSTGRES_PASSWORD}@${process.env.POSTGRES_HOST}:${process.env.POSTGRES_PORT}/${process.env.POSTGRES_DB_NAME}`;
const db = pgp(connection_string);

module.exports = db;
