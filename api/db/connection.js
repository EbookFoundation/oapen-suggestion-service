const options = {};
const pgp = require("pg-promise")(options);
const fs = require("fs");

class DatabaseConnectionError extends Error {
  constructor(message) {
    super(message);
  }
}

let db;

try {
  const cn = {
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    database: process.env.POSTGRES_DB_NAME,
    user: process.env.POSTGRES_USERNAME,
    password: process.env.POSTGRES_PASSWORD,
    ssl: {
	    rejectUnauthorized: process.env.POSTGRES_SSLMODE === "require",
	    ca: fs.readFileSync(process.env.CA_CERT).toString(),
    }
  };
  db = pgp(cn);
} catch (e) {
  throw new DatabaseConnectionError(
    "Postgres connection could not be created, please check your .env file."
  );
}

module.exports = db;
