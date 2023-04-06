const validate = require("../validate.js");
const { ParameterizedQuery: PQ } = require("pg-promise");

const db = require("./connection.js");

async function querySuggestions(handle, threshold = 0) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: `SELECT s.*
    FROM (SELECT handle, unnest(suggestions::oapen_suggestions.suggestion[]) AS suggestion 
    FROM oapen_suggestions.suggestions) s
    WHERE handle = $1
    AND (s.suggestion).similarity >= $2`,
    values: [handle, threshold],
  });

  let result = await db.many(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });

  if (result?.["error"])
    return result;
  
  const data = {
    "handle": handle,
    "suggestions": result.map((e) => {return e["suggestion"];})
  };
  
  return data;
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
