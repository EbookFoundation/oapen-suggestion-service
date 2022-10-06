const express = require("express");
const app = express();
const apiRoutes = require("routes");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", apiRoutes);

app.use("*", (req, res) => {
  res.status(404).json({ error: "Resource not found" });
});

app.listen(3000, () => {
  console.log("Suggestion Service API is up!");
});
