const options = {};
const pgp = require("pg-promise")(options);

const connection = require("./database.js");

const db = pgp(connection);

module.exports = db;
