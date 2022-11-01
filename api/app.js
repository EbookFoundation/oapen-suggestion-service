require("dotenv").config({ path: "./config.env" });
const express = require("express");
const app = express();

const apiRoutes = require("./routes.js");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", apiRoutes);

app.use("*", (req, res) => {
  return res.status(404).json({ error: "Resource not found" });
});

const port = process.env.PORT || 3001;

app.listen(port, () => {
  console.log("Suggestion Service API is up on port " + port);
  console.log("Endpoint: /GET http://localhost:" + port + "/api/{handle}");
  console.log("Endpoint: /GET http://localhost:" + port + "/api/{handle}/ngrams")
});
