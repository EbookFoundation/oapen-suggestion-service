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
        self.text = text


Suggestion = Tuple[str, float]
SuggestionRowWithoutDate = Tuple[str, str, List[Suggestion]]
SuggestionRowWithDate = Tuple[str, str, List[Suggestion], datetime, datetime]
SuggestionRow = Union[SuggestionRowWithDate, SuggestionRowWithoutDate]

Ngram = Tuple[str, int]
NgramRowWithoutDate = Tuple[str, List[Ngram]]
NgramRowWithDate = Tuple[str, List[Ngram], datetime, datetime]
NgramRow = Union[NgramRowWithDate, NgramRowWithoutDate]

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
