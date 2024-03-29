import re
import string
from typing import List

from .oapen_types import (  # pylint: disable=relative-beyond-top-level
    NgramDict,
    NgramRow,
    OapenItem,
)

import nltk
import pandas as pd
from nltk import word_tokenize

from .stopwords_processor import STOPWORDS

nltk.download("punkt")

def process_text(text):
    p_text = "".join([c for c in text.lower() if c not in string.punctuation])
    stopwords_regex = re.compile(r"\b%s\b" % r"\b|\b".join(map(re.escape, STOPWORDS)))
    p_text = stopwords_regex.sub("", p_text)
    words = word_tokenize(p_text)
    filtered_words = list(
        filter(lambda x: x.isalpha(), words)
    )  # added isalpha to check that it contains only letters
    return filtered_words


def sort_ngrams_by_count(ngrams: NgramDict):
    return sorted(ngrams.items(), key=lambda item: item[1], reverse=True)


def generate_ngram(text, n=3) -> NgramDict:
    ngrams = {}
    # store appearance count of each trigram
    for index in range(0, len(text) + 1 - n):
        ngram = " ".join(text[index : index + n])
        ngrams.setdefault(ngram, 0)  # sets curr ngram to 0 if non-existant
        ngrams[ngram] += 1
    return dict(sort_ngrams_by_count(ngrams))  # return sorted by count


def get_n_most_occuring(dic: NgramDict, n=100):
    sorted_dict = dict(
        sort_ngrams_by_count(dic)
    )  # sorts in case of additionas post generate_ngram
    return list(sorted_dict)[:n]


# Currently, this uses the n most occuring ngrams to compare
# This could also count the instances in the highest
def get_similarity_score(
    ngram1: NgramDict, ngram2: NgramDict, n=100, as_percent=True
) -> float:
    n_most_occ_1 = get_n_most_occuring(ngram1, n)
    n_most_occ_2 = get_n_most_occuring(ngram2, n)
    repeated = 0
    for n_gram in n_most_occ_1:
        if n_gram in n_most_occ_2:
            repeated += 1
    return repeated / n if as_percent else repeated


# this treats ngrams1 as primary ngrams, since we want a
# 100% similarity score if all ngrams match from book 1
# this means that a fragment of a book will get a 100% similarity score
# when compared to it's own book, but not the reverse interaction
def get_similarity_score_by_dict_count(ngrams1: NgramDict, ngrams2: NgramDict) -> float:
    repeated = 0
    total = sum(ngrams1.values())  # gets counts from book 1
    for key, ngrams1_value in ngrams1.items():
        repeated += min(
            ngrams1_value, ngrams2.get(key, 0)
        )  # adds min value, or 0 by default if key not found
        # if(min(ngrams1_value, ngrams2.get(key, 0)) != 0):
        #     print(key)
    return repeated / total


def get_ngrams_for_items(items: List[OapenItem], n=3, ngram_limit=30) -> List[NgramRow]:
    rows = []
    for item in items:
        text = process_text(item.text)
        ngrams = generate_ngram(text, n)
        row = NgramRow(
            handle=item.handle,
            name=item.name,
            thumbnail=item.thumbnail,
            ngrams=list(sort_ngrams_by_count(ngrams))[0:ngram_limit],
        )
        rows.append(row)
    return rows
