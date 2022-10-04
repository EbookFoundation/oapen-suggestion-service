import type { GetStaticProps, GetStaticPaths } from "next";
import { OAPENItems } from "../../lib/oapen";
import type { OAPENItemWithMetadata } from "../../lib/oapen/OAPENTypes";

interface SingleItemProps {
  item: OAPENItemWithMetadata;
}

export default function ItemSingle({ item }: SingleItemProps) {
  const name = item.metadata.find(({ key }) => key == "grantor.name")?.value;
  return (
    <>
      <h1>{name}</h1>
      <code>
        <pre>{JSON.stringify({ item }, null, 4)}</pre>
      </code>
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
  const item = await OAPENItems.getItemWithMetadata(context?.params?.uuid + "");
  const data: SingleItemProps = {
    item,
  };

  return {
    props: {
      ...data,
    },
  };
};
