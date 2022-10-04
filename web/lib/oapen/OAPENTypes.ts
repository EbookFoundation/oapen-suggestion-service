export type OAPENTypeID = string;
export type OAPENHandle = string;
export type OAPENType = string;
export type OAPENExpandable = string;
export type OAPENBitstreams = string;
export type OAPENApiRelativePath = string;
export type URL = string;

export interface Expandable {
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
