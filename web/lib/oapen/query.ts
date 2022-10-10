const ENDPOINT = "https://library.oapen.org/rest";
import axios from "axios";

export async function get(url = "") {
  const post_url = [ENDPOINT, url].join("/");
  const text = (await axios.get(post_url)).data;
  return text;
}
