const validate = require("../validate.js");
const { ParameterizedQuery: PQ } = require("pg-promise");

const db = require("./connection.js");

async function querySuggestions(handle) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: "SELECT * FROM oapen_suggestions.suggestions WHERE handle = $1",
    values: [handle],
  });

  return db.one(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });
}

async function queryNgrams(handle) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: "SELECT * FROM oapen_suggestions.ngrams WHERE handle = $1",
    values: [handle],
  });

  return db.one(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });

  // return await db.any(query);
}

module.exports = {
  querySuggestions,
  queryNgrams,
};
