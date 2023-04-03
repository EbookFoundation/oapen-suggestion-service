from typing import List

import data.oapen as OapenAPI
from model.oapen_types import OapenItem


def test_get_item():
    item = OapenAPI.get_item("20.500.12657/47586")
    assert isinstance(item, OapenItem)
    assert item.name == "Embodying Contagion"


def test_get_item_404():
    item: List[OapenItem] = OapenAPI.get_item("20.400.12657/47581")
    assert len(item) == 0


def test_get_collection_limit():
    collection = OapenAPI.get_collection_items_by_label(
        "Knowledge Unlatched (KU)", limit=10
    )
    assert len(collection) <= 10


def test_get_collection_404():
    collection = OapenAPI.get_collection_items_by_label("hahaha", limit=10)
    assert len(collection) == 0
