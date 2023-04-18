const express = require("express");
const router = express.Router();
const validate = require("./validate");
const pgp = require("pg-promise");
const data = require("./db/data.js");

//GET endpoint for suggestions
router.get("/:handle([0-9]+.[0-9]+.[0-9]+/[0-9]+)", async (req, res) => {
  try {
    let handle = req.params.handle;
    let threshold = parseInt(req.query.threshold) || 0;

    await validate.checkHandle(handle);

    let responseData = await data.querySuggestions(handle, threshold);

    if (
      responseData?.["error"] &&
      responseData?.["error"]?.name === pgp.errors.QueryResultError.name
    ) {
      return res.status(404).json({ error: responseData?.["error"].message });
    } else if (responseData?.["error"]) {
      return res.status(500).json(responseData);
    }

    res.header("Access-Control-Allow-Origin", "*");

    res.status(200).json({
      items: responseData,
    });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: "Internal server error" });
  }
});

//GET endpoint for ngrams
router.get("/:handle([0-9]+.[0-9]+.[0-9]+/[0-9]+)/ngrams", async (req, res) => {
  try {
    const handle = req.params.handle;
    await validate.checkHandle(handle);

    let responseData = await data.queryNgrams(handle);

    if (
      responseData.error &&
      responseData.error.name === pgp.errors.QueryResultError.name
    ) {
      return res.status(404).json({ error: responseData.error.message });
    } else if (responseData.error) {
      return res.status(500).json(responseData);
    }

    res.header("Access-Control-Allow-Origin", "*");

    return res.status(200).json(responseData);
  } catch (e) {
    return res.status(500).json({ error: "Internal server error" });
  }
});

router.get("/", async (req, res) => {
  try {
    let threshold = parseInt(req.query.threshold) || 0;
    if (threshold < 0) threshold = 0;
    let limit = parseInt(req.query.limit) || validate.DEFAULT_ITEM_LIMIT;
    let offset = parseInt(req.query.offset) || 0;
    if (limit > validate.MAX_ITEM_LIMIT) {
      limit = validate.MAX_ITEM_LIMIT;
    } else if (limit < 1) {
      limit = 1;
    }
    if (offset < 0) offset = 0;


    let responseData = await data.queryManySuggestions(threshold, limit, offset);

    if (
      responseData.error &&
      responseData.error.name === pgp.errors.QueryResultError.name
    ) {
      return res.status(404).json({ error: responseData.error.message });
    } else if (responseData.error) {
      return res.status(500).json(responseData);
    }

    res.header("Access-Control-Allow-Origin", "*");

    return res.status(200).json(responseData);
  } catch (e) {
    return res.status(500).json({ error: "Internal server error" });
  }
})

router.get("/ngrams", async (req, res) => {
  try {
    let limit = parseInt(req.query.limit) || validate.DEFAULT_ITEM_LIMIT;
    let offset = parseInt(req.query.offset) || 0;
    if (limit > validate.MAX_ITEM_LIMIT) {
      limit = validate.MAX_ITEM_LIMIT;
    } else if (limit < 1) {
      limit = 1;
    }
    if (offset < 0) offset = 0;

    let responseData = await data.queryManyNgrams(limit, offset);

    if (
      responseData.error &&
      responseData.error.name === pgp.errors.QueryResultError.name
    ) {
      return res.status(404).json({ error: responseData.error.message });
    } else if (responseData.error) {
      return res.status(500).json(responseData);
    }

    res.header("Access-Control-Allow-Origin", "*");

    return res.status(200).json(responseData);
  } catch (e) {
    return res.status(500).json({ error: "Internal server error" });
  }
})

module.exports = router;
