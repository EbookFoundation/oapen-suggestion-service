const FETCH_URL_HOST = "http://159.65.185.229:3001";

async function mountSuggestions() {
  // get element to mount suggestions engine to: mount-suggestions
  const mountElement = document.getElementById("mount-suggestions");
  // if there's no element to mount to, console error and return
  if (!mountElement) {
    console.error("No element to mount suggestions engine to!");
    return;
  }

  const url = (handle) => FETCH_URL_HOST + "/api/" + handle;

  // get handle from property on mount element
  // TODO also get from URL
  const handle = mountElement.getAttribute("data-handle");

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

  const handles = suggestions.map((suggestion) =>
    suggestion.split(",")[0].substring(1).trim()
  );
  // create suggestions element

  const suggestionsElement = document.createElement("div");
  suggestionsElement.className = "suggestions";

  // create suggestions list element
  const suggestionsListElement = document.createElement("ul");
  suggestionsListElement.className = "suggestions-list";

  // create suggestions list items
  const suggestionsListItems = handles.map((handle) => {
    const listItem = document.createElement("li");
    listItem.className = "suggestions-list-item";
    // make it a link
    const link = document.createElement("a");
    link.className = "suggestions-list-item-link";
    link.href = "https://library.oapen.org/handle/" + handle;
    link.target = "_blank";
    // TODO change link text to name and icon
    link.innerText = handle;
    listItem.appendChild(link);
    return listItem;
  });

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
};
