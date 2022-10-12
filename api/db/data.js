const validate = require("../validate.js");
const { ParameterizedQuery: PQ } = require("pg-promise");

const db = require("./connection.js");

async function querySuggestions(id) {
  await validate.checkHandle(id);

  // Create a parameterized query with the id
  const query = new PQ({ text: "SELECT * FROM oapen_suggestions.suggestions WHERE item_id = $1", values: [id] });

  // Run query
  return db.one(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });
}

let exportedMethods = {
  async getSuggestions(id) {
    const res = await querySuggestions(id);
    return res;
  },
};

module.exports = exportedMethods;
