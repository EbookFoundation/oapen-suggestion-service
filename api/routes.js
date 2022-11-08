const express = require("express");
const router = express.Router();
const validate = require("./validate");
const pgp = require("pg-promise");

const data = require("./db/data.js");

//GET endpoint
router.get("/:handle", async (req, res) => {
  try {
    var handle = req.params.handle;
    await validate.checkHandle(handle);

    let responseData = await data.querySuggestions(handle);

    if (
      responseData.error &&
      responseData.error.name === pgp.errors.QueryResultError.name
    ) {
      res.status(404).json({ error: responseData.error.message });
      return;
    } else if (responseData.error) {
      res.status(500).json(responseData);
      return;
    }

    res.status(200).json(responseData);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
