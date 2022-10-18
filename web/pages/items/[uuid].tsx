import type { GetStaticProps, GetStaticPaths } from "next";
import { OAPENItems } from "../../lib/oapen";
import { SelfItems } from "../../lib/self";
import type { OAPENItemWithMetadata } from "../../lib/oapen/OAPENTypes";
import { RenderItem } from "../../components/render/RenderItem";

interface SingleItemProps {
  item: OAPENItemWithMetadata;
  selfSuggestions: any; // TODO change
}

export default function ItemSingle({ item }: SingleItemProps) {
  const name =
    item.name || item.metadata.find(({ key }) => key == "grantor.name")?.value;
  const type = item.metadata.find(({ key }) => key == "dc.type")?.value;
  console.log({ item });
  return (
    <>
      <RenderItem item={item} />
    </>
  );
}

// TODO update
export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [],
    fallback: "blocking", // can also be true or 'blocking
  };
};

export const getStaticProps: GetStaticProps<SingleItemProps> = async (
  context
) => {
  // TODO write async
  const item = await OAPENItems.getItemWithMetadata(context?.params?.uuid + "");
  let selfSuggestions = {};
  try {
    selfSuggestions = await SelfItems.getItemByHandle(item?.handle || "");
  } catch (e) {
    console.error("Could not fetch SelfSuggestions", e);
  }

  const data: SingleItemProps = {
    item,
    selfSuggestions,
  };

  return {
    props: {
      ...data,
    },
  };
};
