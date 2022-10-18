import { get } from "./query";
import { SelfSuggestions } from "./SelfTypes"

export const getItemByHandle = async (handle: string): Promise<SelfSuggestions> => {
  const rawText = await get("/" + encodeURIComponent(handle));

  return rawText as SelfSuggestions;
};
