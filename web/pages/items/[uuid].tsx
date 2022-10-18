import type { GetStaticProps, GetStaticPaths } from "next";

import { RenderItem } from "../../components/render/RenderItem";
import { fetchSingleItemProps, SingleItemProps } from "../../lib/item/single";

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
  const uuid = context?.params?.uuid;
  if (!uuid)
    return {
      props: {},
      notFound: true,
    };

  try {
    // TODO may be better to statically render OAPEN data,
    // and ping for suggestions dynamically (lazy load)
    let data = await fetchSingleItemProps(String(uuid));

    if (!data?.item?.handle)
      return {
        props: {},
        notFound: true,
      };

    return {
      props: {
        ...data,
      },
    };
  } catch (e) {
    console.error(e);
    return { props: {}, error: e };
  }
};
