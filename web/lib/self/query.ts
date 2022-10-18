const ENDPOINT = process.env?.API_SERVER || "http://localhost:3001";
import axios from "axios";

export async function get(url = "") {
  const post_url = [ENDPOINT, url].join("/");
  const text = (await axios.get(post_url)).data;
  return text;
}
