const express = require("express");
const router = express.Router();
const validate = require("./validate");

const data = require("./db/data.js");

//GET endpoint
router.get("/:handle", async (req, res) => {
  try {
    var handle = req.params.handle;

    //Validate the parameter
    await validate.checkHandle(handle);

    //Get the data
    let responseData = await data.getSuggestions(handle);

    if (responseData.error && responseData.error.name === "QueryResultError") {
      res.status(404).json({ error: responseData.error.message });
      return;
    } else if (responseData.error) {
      res.status(500).json(responseData);
      return;
    }

    res.status(200).json(responseData);
  } catch (e) {
    res.status(500).json({ error: "Internal server error." });
  }
});

module.exports = router;
