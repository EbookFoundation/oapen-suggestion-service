from datetime import datetime
from typing import Dict, List, NamedTuple


class OapenItem(NamedTuple):
    handle: str
    name: str
    thumbnail: str
    text: str

    def __eq__(self, other):
        return self.handle == other.handle

    def __hash__(self):
        return hash(self.handle, "handle")

class SuggestionRow(NamedTuple):
    handle: str
    suggestion: str
    suggestion_name: str
    suggestion_thumbnail: str
    score: int
    created_at: datetime = None
    updated_at: datetime = None

    def __eq__(self, other):
        return self.handle == other.handle and self.suggestion == other.suggestion

    def __hash__(self) -> int:
        return hash((self.handle, self.suggestion))

class Ngram(NamedTuple):
    ngram: str
    count: int

class NgramRow(NamedTuple):
    handle: str
    name: str
    thumbnail: str
    ngrams: List[Ngram]
    created_at: datetime = None
    updated_at: datetime = None

    def __eq__(self, other):
        return self.handle == other.handle

    def __hash__(self) -> int:
        return hash(self.handle)


NgramDict = Dict[str, int]


class UrlRow(NamedTuple):
    url: str
    completed: bool
    updated_at: datetime = None
