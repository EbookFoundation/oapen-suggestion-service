from datetime import datetime
from typing import Dict, List, Tuple, Union


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

        language = list(filter(lambda x: x["key"] == "dc.language", self.metadata))
        self.language = None if len(language) == 0 else language[0]["value"]
        self.text = text

    def __eq__(self, other):
        return self.handle == other.handle

    def __hash__(self):
        return hash(self.handle, "handle")


SuggestionRowWithoutDate = Tuple[str, str, str, int]
SuggestionRowWithDate = Tuple[str, str, str, int, datetime, datetime]
SuggestionRow = Union[SuggestionRowWithDate, SuggestionRowWithoutDate]

Ngram = Tuple[str, int]
NgramRowWithoutDate = Tuple[str, List[Ngram]]
NgramRowWithDate = Tuple[str, List[Ngram], datetime, datetime]
NgramRow = Union[NgramRowWithDate, NgramRowWithoutDate]

NgramDict = Dict[str, int]

UrlRow = Tuple[str, bool]


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
