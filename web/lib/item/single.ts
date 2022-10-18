import { OAPENItems } from "../oapen";
import { SelfItems } from "../self";
import type { OAPENItemWithMetadata } from "../oapen/OAPENTypes";

export interface SingleItemProps {
  item?: OAPENItemWithMetadata;
  selfSuggestions?: any; // TODO change
}

export const fetchSingleItemProps = async (
  uuid: string
): Promise<SingleItemProps> => {
  const item = await OAPENItems.getItemWithMetadata(uuid + "");
  let selfSuggestions = null;
  try {
    selfSuggestions = await SelfItems.getItemByHandle(item?.handle || "");
  } catch (e) {
    console.error("Could not fetch SelfSuggestions", e);
  }

  const data: SingleItemProps = {
    item,
    selfSuggestions,
  };

  return data;
};
