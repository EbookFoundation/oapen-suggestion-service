const options = {};
const pgp = require("pg-promise")(options);

var connection;

try {
  connection = require("./database.js");
} catch (e) {
  //No database.js file was found. Use database.env instead
  connection = process.env.DATABASE_URL || "postgres://username:password@host:port/database";
}

const db = pgp(connection);

module.exports = db;
