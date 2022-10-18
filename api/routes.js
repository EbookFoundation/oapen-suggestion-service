const express = require("express");
const router = express.Router();
const validate = require("./validate");

router.get("/:handle", async (req, res) => {
  try {
    await validate.checkHandle(req.params.handle);
    //TODO: Call a data function to grab suggestions from DB
    let responseData = { error: "Not implemented" };
    res.status(500).json(responseData);
    return;
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Something happened" });
    return;
  }
});

module.exports = router;
