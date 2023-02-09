const express = require("express");
const router = express.Router();
const validate = require("./validate");
const pgp = require("pg-promise");
const data = require("./db/data.js");

//GET endpoint for suggestions
router.get("/:handle([0-9]+.[0-9]+.[0-9]+/[0-9]+)", async (req, res) => {
  try {
    let handle = req.params.handle;
    await validate.checkHandle(handle);

    let responseData = await data.querySuggestions(handle);

    if (
      responseData?.["error"] &&
      responseData?.["error"]?.name === pgp.errors.QueryResultError.name
    ) {
      return res.status(404).json({ error: responseData?.["error"].message });
    } else if (responseData?.["error"]) {
      return res.status(500).json(responseData);
    }

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

    return res.status(200).json(responseData);
  } catch (e) {
    return res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
