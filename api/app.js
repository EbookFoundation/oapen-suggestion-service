const express = require("express");
const path = require("path");
const app = express();

const apiRoutes = require("./routes.js");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", apiRoutes);

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");

  next();
});

app.use("*", (req, res) => {
  return res.status(404).json({ error: "Resource not found" });
});

const port = process.env.API_PORT || 8000;

app.listen(port, () => {
  console.log("Suggestion Service API is up on port " + port);
  console.log("Running at http://localhost:" + port + "/api");
});
