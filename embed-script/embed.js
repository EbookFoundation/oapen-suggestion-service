const FETCH_URL_HOST = "http://159.65.185.229:3001";

async function mountSelfData() {
  const metadata = (handle) =>
    "http://localhost:3002" + "/metadata/" + encodeURIComponent(handle);

  // pattern should be in URL: /handle/[handle]
  if (!window.location.pathname.includes("/handle/")) {
    console.error("No handle found in URL!");
    return;
  }

  const _handle = window.location.pathname.split("/handle/")[1];
  // should only contain one slash
  const [hnd1, hnd2] = _handle.split("/");
  const handle = [hnd1, hnd2].join("/");

  if (!handle) {
    console.error("No handle found!");
    return;
  }

  const response = await fetch(metadata(handle));

  const resp = await response.json();

  console.log("self", resp[0]);

  const { name } = resp[0];

  // put name in ds-dc_contributor_author-authority

  const authorElement = document.querySelector(
    ".ds-dc_contributor_author-authority"
  );

  if (!authorElement) {
    console.error("No author element found!");
    return;
  }

  authorElement.innerText = name;
}

async function mountSuggestions() {
  // get element to mount suggestions engine to: mount-suggestions
  const mountElement = document.querySelector(".col-sm-4");
  // if there's no element to mount to, console error and return
  if (!mountElement) {
    console.error("No element to mount suggestions engine to!");
    return;
  }

  // pattern should be in URL: /handle/[handle]
  if (!window.location.pathname.includes("/handle/")) {
    console.error("No handle found in URL!");
    return;
  }

  const _handle = window.location.pathname.split("/handle/")[1];
  // should only contain one slash
  const [hnd1, hnd2] = _handle.split("/");
  const handle = [hnd1, hnd2].join("/");

  if (!handle) {
    console.error("No handle found!");
    return;
  }

  const url = (handle) => FETCH_URL_HOST + "/api/" + handle;

  // fetch suggestions from API
  const response = await fetch(url(handle));
  const resp = await response.json();

  if (!resp.items || !resp?.items?.suggestions) {
    console.error("No items in response!");
    return;
  }

  const { suggestions } = resp.items;

  if (suggestions.length === 0) {
    console.error("No suggestions in response!");
    return;
  }

  // parse suggestions -- v1

  if (!(suggestions[0].includes(",") && suggestions[0].startsWith("("))) {
    console.log("Schema has changed for suggestions, could not mount!");
    return;
  }

  // add in col-sm-4
  // create an additional item-page-field-wrapper child

  const handles = suggestions.map((suggestion) =>
    suggestion.split(",")[0].substring(1).trim()
  );
  // create suggestions element

  const suggestionsElement = document.createElement("div");
  suggestionsElement.className = "item-page-field-wrapper child";
  suggestionsElement.id = "suggestions";

  // <h5>Related</h5>
  const relatedElement = document.createElement("h5");
  relatedElement.innerText = "Related";
  suggestionsElement.appendChild(relatedElement);

  // create suggestions list element
  const suggestionsListElement = document.createElement("ul");
  suggestionsListElement.className = "suggestions-list";

  // promise all get metadata for each handle

  const metadata = (handle) =>
    "http://localhost:3002" + "/metadata/" + encodeURIComponent(handle);

  const fetchMetadata = async (handle) => {
    const res = await fetch(metadata(handle));

    // return json
    return await res.json();
  };

  // get all promise all
  const responses = await Promise.all(
    handles.map((handle) => fetchMetadata(handle))
  );

  console.log(responses);

  // create suggestions list items
  let suggestionsListItems = handles.map((handle, i) => {
    const listItem = document.createElement("li");
    listItem.className = "suggestions-list-item";
    // make it a link
    const link = document.createElement("a");
    link.className = "suggestions-list-item-link";
    link.href = "/handle/" + handle;
    link.target = "_blank";

    const meta = responses[i];

    const name = meta[0]?.name;

    // TODO change link text to name and icon
    link.innerText = name || handle;

    listItem.appendChild(link);
    return listItem;
  });

  // pick only first 4 or less suggestionsListItems
  if (suggestionsListItems.length > 4) {
    // get first 4
    suggestionsListItems = suggestionsListItems.slice(0, 4);
  }

  // append suggestions list items to list
  suggestionsListItems.forEach((item) =>
    suggestionsListElement.appendChild(item)
  );

  // append list to suggestions element
  suggestionsElement.appendChild(suggestionsListElement);

  // append suggestions element to mount element
  mountElement.appendChild(suggestionsElement);
}

window.onload = function () {
  mountSuggestions();
  mountSelfData();
};
