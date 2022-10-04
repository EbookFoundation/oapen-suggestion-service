import type {
  OAPENItemQueried,
  OAPENExpandable,
  OAPENApiRelativePath,
  OAPENType,
  OAPENTypeID,
  OAPENItemRaw,
  RawMetadataItem,
  OAPENItemWithMetadata,
} from "./OAPENTypes";
import { get } from "./query";

const transformRawItemQueried = (item: any) => {
  return {
    uuid: item.uuid as OAPENTypeID,
    name: (item?.name || "") as string,
    handle: item?.handle as string,
    type: item?.type as OAPENType,
    // comes in sometimes as string or boolean, if null return false
    archived: Boolean(item?.archived),
    withdrawn: Boolean(item?.withdrawn),
    link: item?.link as OAPENApiRelativePath,
    expand: item?.expand as OAPENExpandable[],
  } as OAPENItemQueried;
};

export const getItemsRaw = async (): Promise<OAPENItemQueried[]> => {
  const rawText = await get("items");

  const transformed = rawText.map(
    transformRawItemQueried
  ) as OAPENItemQueried[];

  return transformed;
};

export const getItemSingleRaw = async (
  uuid: string
): Promise<OAPENItemQueried> => {
  const rawText = await get(["items", uuid].map(encodeURIComponent).join("/"));

  const transformed = transformRawItemQueried(rawText);

  return transformed;
};

export const getItemSingleMetadata = async (
  uuid: string
): Promise<RawMetadataItem[]> => {
  const rawText = await get(
    ["items", uuid, "metadata"].map(encodeURIComponent).join("/")
  );
  return rawText as RawMetadataItem[];
};

export const combineItemMetadata = (
  item: OAPENItemQueried,
  metadata: RawMetadataItem[]
): OAPENItemWithMetadata => {
  return { ...item, metadata } as OAPENItemWithMetadata;
};
export const getItemWithMetadata = async (
  uuid: string
): Promise<OAPENItemWithMetadata> => {
  const [item, metadata] = await Promise.all([
    getItemSingleRaw(uuid),
    getItemSingleMetadata(uuid),
  ]);
  return combineItemMetadata(item, metadata);
};
