import data.oapen as OapenAPI


def test_get_collection_limit():
    collection = OapenAPI.get_collection_items_by_id(
        "ea93f8f0-430f-4a03-b7e2-5b06053585b0", limit=10
    )
    assert len(collection) <= 10


def test_get_collection_404():
    collection = OapenAPI.get_collection_items_by_id("hahaha", limit=10)
    assert collection is None
