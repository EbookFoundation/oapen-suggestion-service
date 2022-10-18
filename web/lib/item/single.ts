import { OAPENItems } from "../oapen";
import { SelfItems } from "../self";
import type { OAPENItemWithMetadata } from "../oapen/OAPENTypes";
import type { SelfSuggestions } from "../self/SelfTypes";

export interface SingleItemProps {
  item?: OAPENItemWithMetadata;
  selfSuggestions?: SelfSuggestions;
  lastFetchedTogether?: number;
}

export const fetchSingleItemProps = async (
  uuid: string
): Promise<SingleItemProps> => {
  const [item, selfSuggestions] = await Promise.all([
    OAPENItems.getItemWithMetadata(uuid + ""),
    SelfItems.getItemByHandle(uuid || "").catch((e) => {
      console.error(e);
      return null;
    }),
  ]);

  const data: SingleItemProps = {
    item,
    selfSuggestions,
    lastFetchedTogether: Date.now(),
  };

  return data;
};
