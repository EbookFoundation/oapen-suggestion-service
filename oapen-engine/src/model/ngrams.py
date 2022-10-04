import string
from typing import List

import nltk
import pandas as pd

import data.oapen as OapenAPI
import lib.stopwords as oapen_stopwords

from .oapen_types import OapenItem, transform_item_data

nltk.download("stopwords")
from nltk import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = (
    stopwords.words("english")
    + stopwords.words("german")
    + stopwords.words("dutch")
    + oapen_stopwords.stopwords_dutch_extra
    + oapen_stopwords.stopwords_filter
    + oapen_stopwords.stopwords_publisher
)


def process_text(text):
    l_text = text.lower()
    p_text = "".join([c for c in l_text if c not in string.punctuation])
    words = word_tokenize(p_text)
    filtered_words = list(filter(lambda x: x not in STOPWORDS, words))

    return filtered_words


def get_data(collection_limit=1, item_limit=10) -> List[OapenItem]:
    books_collections = OapenAPI.get_collections_from_community(
        OapenAPI.BOOKS_COMMUNITY_ID
    )
    books_items = []

    for i in range(min(collection_limit, len(books_collections))):
        books_items += OapenAPI.get_items_from_collection(books_collections[i])

    items = []

    for i in range(0, min(item_limit, len(books_items))):
        book_item = OapenAPI.get_item(books_items[i])
        item = transform_item_data(book_item)
        items.append(item)
    return items


def make_df(data: List[OapenItem]):
    df = pd.DataFrame(columns=["uuid", "name", "text"])
    for item in data:
        text = process_text(item.get_text_bitstream())
        df.loc[len(df.index)] = [item.uuid, item.name, text]
    return df


def run_ngrams():
    data = get_data()
    df = make_df(data)
    print(df.shape)
    print(df[:10])
