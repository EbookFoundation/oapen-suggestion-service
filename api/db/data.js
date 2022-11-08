const validate = require("../validate.js");
const { ParameterizedQuery: PQ } = require("pg-promise");

const db = require("./connection.js");

async function querySuggestions(handle) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: "SELECT * FROM oapen_suggestions.suggestions WHERE handle = $1 LIMIT 2",
    values: [handle],
  });

  return await db.any(query);
}

module.exports = {
  querySuggestions,
};
