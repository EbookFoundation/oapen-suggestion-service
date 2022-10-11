const express = require("express");
const router = express.Router();
const validate = require("./validate");

const data = require("./db/data");

router.get("/:handle", async (req, res) => {
  try {
    var handle = req.params.handle;
    await validate.checkHandle(handle);

    let responseData = await data.getSuggestions(handle);
    console.log(responseData);

    res.status(200).json(responseData);
  } catch (e) {
    res.status(200).json({});
  }
});

module.exports = router;
