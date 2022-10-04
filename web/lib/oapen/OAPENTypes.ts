export type OAPENTypeID = string;
export type OAPENHandle = string;
export type OAPENType = string;
export type OAPENExpandable = string;
export type OAPENBitstreams = string;
export type OAPENApiRelativePath = string;
export type URL = string;

export interface Expandable {
  // OAPEN returns a list of "expandables" -- things you can further query for additionally (like metadata). Once the expandable is added to the object, it's removed from this list.
  expand?: OAPENExpandable[];
}

export interface OAPENItemRaw {
  uuid: OAPENTypeID;
  name?: string;
  handle?: OAPENHandle;
  type?: OAPENType;
  archived: boolean;
  withdrawn: boolean;
  link?: OAPENApiRelativePath;
}

export interface RawMetadataItem {
  key: string;
  value: string;
  qualifier?: string;
  language?: string;
  element?: string;
}

type HasMetadata = {
  metadata: RawMetadataItem[];
};

export type OAPENItemQueried = OAPENItemRaw & Expandable;
export type OAPENItemWithMetadata = OAPENItemQueried & HasMetadata;
