const validate = require("../validate.js");
const { ParameterizedQuery: PQ } = require("pg-promise");

const db = require("./connection.js");

async function querySuggestions(handle, threshold = 0) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: `SELECT suggestion AS handle, score
    FROM oapen_suggestions.suggestions
    WHERE handle = $1
    AND score >= $2`,
    values: [handle, threshold],
  });

  let result = await db.many(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });

  if (result?.["error"]) return result;

  console.log(result);

  const data = {
    handle: handle,
    suggestions: result,
  };

  return data;
}

async function queryNgrams(handle) {
  await validate.checkHandle(handle);

  const query = new PQ({
    text: `SELECT handle, "name", thumbnail, created_at, updated_at,
    array_agg(
      JSON_BUILD_OBJECT(
        'ngram', ngram.ngram,
        'count', ngram.count
      )
    ) as ngrams
    FROM oapen_suggestions.ngrams, UNNEST(ngrams) as ngram
    WHERE handle = $1
    GROUP BY handle;`,
    values: [handle],
  });

  return db.one(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });
}

async function queryManySuggestions(
  threshold = 0,
  limit = validate.DEFAULT_ITEM_LIMIT,
  offset = 0
) {
  if (threshold < 0) threshold = 0;
  if (limit > validate.MAX_ITEM_LIMIT) {
    limit = validate.MAX_ITEM_LIMIT;
  } else if (limit < 1) {
    limit = 1;
  }
  if (offset < 0) offset = 0;

  const query = new PQ({
    text: `SELECT suggestion AS handle, score
    FROM oapen_suggestions.suggestions
    WHERE score >= $1
    ORDER BY created_at DESC
    LIMIT $2 OFFSET $3;`,
    values: [threshold, limit, offset],
  });

  return db.query(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });
}

async function queryManyNgrams(limit = validate.DEFAULT_ITEM_LIMIT, offset = 0) {
  if (limit > validate.MAX_ITEM_LIMIT) {
    limit = validate.MAX_ITEM_LIMIT;
  } else if (limit < 1) {
    limit = 1;
  }
  if (offset < 0) offset = 0;

  const query = new PQ({
    text: `SELECT handle, "name", thumbnail, created_at, updated_at,
    array_agg(
      JSON_BUILD_OBJECT(
        'ngram', ngram.ngram,
        'count', ngram.count
      )
    ) as ngrams
    FROM oapen_suggestions.ngrams, UNNEST(ngrams) as ngram
    GROUP BY handle
    ORDER BY created_at
    LIMIT $1 OFFSET $2;
    `,
    values: [limit, offset],
  });

  return db.query(query).catch((error) => {
    return { error: { name: error.name, message: error.message } };
  });
}

module.exports = {
  querySuggestions,
  queryNgrams,
  queryManySuggestions,
  queryManyNgrams,
};
