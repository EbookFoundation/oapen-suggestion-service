const options = {};
const pgp = require("pg-promise")(options);

const connection = process.env.DATABASE_URL || "postgres://username:password@host:port/database";

const db = pgp(connection);

module.exports = db;
