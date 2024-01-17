// every request serves index.html except embed.js serves embed.js

const express = require("express");
const app = express();
const path = require("path");
const axios = require("axios");
const xml2js = require("xml2js");

const metadata = (handle) =>
  "https://library.oapen.org/rest/search?query=handle:" + handle;

app.get("/embed.js", (req, res) => {
  res.sendFile(path.join(__dirname, "embed.js"));
});

app.get("/main.css", (req, res) => {
  res.sendFile(path.join(__dirname, "main.css"));
});

app.get("/metadata/:handle", async (req, res) => {
  const handle = req.params.handle;
  const url = metadata(handle);
  // fetch
  const response = await axios.get(url);

  // get response text
  const text = response.data;

  res.send(text);
});

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(3002, () => console.log("Example app listening on port 3002!"));
