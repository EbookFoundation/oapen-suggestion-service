from typing import Dict, List, NewType, Tuple


class OapenItem:
    def __init__(
        self, uuid, name, handle, expand, link, metadata, bitstreams, text: str
    ):
        self.uuid = uuid
        self.name = name
        self.handle = handle
        self.expand = expand
        self.link = link
        self.metadata = metadata
        self.bitstreams = bitstreams
        self.text = text


OapenSuggestion = NewType("OapenSuggestion", Tuple[str, float])
OapenNgram = NewType("OapenNgram", Tuple[str, List[Tuple[str, int]]])

SuggestionRow = NewType("SuggestionRow", Tuple[str, str, List[OapenSuggestion]])

NgramDict = Dict[str, int]


def transform_item_data(item, text) -> OapenItem:
    return OapenItem(
        item["uuid"],
        item["name"],
        item["handle"],
        item["expand"],
        item["link"],
        item["metadata"],
        item["bitstreams"],
        text,
    )


def transform_multiple_items_data(items) -> List[OapenItem]:
    return [transform_item_data(item, item["bitstreams"]) for item in items]
