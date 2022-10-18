import { get } from "./query";

export const getItemByHandle = async (handle: string): Promise<any> => {
  const rawText = await get("/" + encodeURIComponent(handle));

  return rawText;
};
