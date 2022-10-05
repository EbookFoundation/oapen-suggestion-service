const express = require("express");
const router = express.Router();
const validate = require("./validate");

router.get("/:handle", async (req, res) => {
  try {
    await validate.checkHandle(req.params.handle);
    //TODO: Call a data function to grab suggestions from DB
    let responseData = { error: "Not implemented" };
    res.status(200).json(responseData);
  } catch (e) {
    res.status(200).json({});
  }
});

module.exports = router;
