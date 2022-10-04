import { OAPENItemWithMetadata } from "../../lib/oapen/OAPENTypes";
export const RenderItem = ({ item }: { item: OAPENItemWithMetadata }) => {
  const type = item.metadata.find(({ key }) => key == "dc.type")?.value;

  if (type == "book") return <RenderBook book={transformToBook(item)} />;

  return (
    <>
      <h1>Could not render this item with type {type}</h1>
      <br />
      <code>
        <pre>{JSON.stringify(item, null, 4)}</pre>
      </code>
    </>
  );
};
interface InternalBook {
  title?: string;
  author?: string;
  // date
  accessioned?: string;
  issued?: string;
  uri?: string;
  abstract?: string;
  language?: string;
  classification?: string;
  altTitle?: string;
  publisherName?: string;
  pageCount?: string;
  item: OAPENItemWithMetadata;
}
const transformToBook = (item: OAPENItemWithMetadata) => {
  return {
    item,
    title: item.metadata.find(({ key }) => key == "dc.title")?.value,
    author: item.metadata.find(({ key }) => key == "dc.contributor.author")
      ?.value,
    accessioned: item.metadata.find(({ key }) => key == "dc.date.accessioned")
      ?.value,
    issued: item.metadata.find(({ key }) => key == "dc.date.issued")?.value,
    uri: item.metadata.find(({ key }) => key == "dc.identifier.uri")?.value,
    abstract: item.metadata.find(({ key }) => key == "dc.description.abstract")
      ?.value,
    language: item.metadata.find(({ key }) => key == "dc.language")?.value,
    classification: item.metadata.find(
      ({ key }) => key == "dc.subject.classification"
    )?.value,
    altTitle: item.metadata.find(({ key }) => key == "dc.title.alternative")
      ?.value,
    publisherName: item.metadata.find(({ key }) => key == "publisher.name")
      ?.value,
    pageCount: item.metadata.find(({ key }) => key == "oapen.pages")?.value,
  };
};

export const RenderBook = ({ book }: { book: InternalBook }) => {
  return (
    <>
      <h1>{book?.title}</h1>
      <h2>
        by {book?.author} ({book?.pageCount} pages)
      </h2>
      <p>{book?.abstract}</p>
    </>
  );
};
