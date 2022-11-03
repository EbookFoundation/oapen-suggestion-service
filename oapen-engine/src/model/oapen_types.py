from typing import Dict, List, Tuple

import data.oapen as OapenAPI


class OapenItem:
    def __init__(self, uuid, name, handle, expand, link, metadata, bitstreams):
        self.uuid = uuid
        self.name = name
        self.handle = handle
        self.expand = expand
        self.link = link
        self.metadata = metadata
        self.bitstreams = bitstreams

    def get_text(self):
        return OapenAPI.get_bitstream_text(self.bitstreams)


OapenSuggestion = Tuple[str, float]
OapenNgram = Tuple[str, List[Tuple[str, int]]]

NgramDict = Dict[str, int]


def transform_item_data(item) -> OapenItem:
    uuid = item["uuid"]
    name = item["name"]
    handle = item["handle"]
    expand = item["expand"]
    link = item["link"]
    metadata = item["metadata"]
    bitstreams = item["bitstreams"]

    return OapenItem(uuid, name, handle, expand, link, metadata, bitstreams)


def transform_multiple_items_data(data: List[object]) -> List[OapenItem]:
    return [transform_item_data(x) for x in data]
