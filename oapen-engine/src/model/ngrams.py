import string
from typing import List

import data.oapen as OapenAPI # pylint: disable=import-error
import model.stopwords as oapen_stopwords # pylint: disable=import-error
import nltk # pylint: disable=import-error
import pandas as pd # pylint: disable=import-error
from nltk import word_tokenize # pylint: disable=import-error
from nltk.corpus import stopwords # pylint: disable=import-error

from .oapen_types import OapenItem, transform_item_data # pylint: disable=relative-beyond-top-level

nltk.download("stopwords")

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
    filtered_words = list(filter(lambda x: x not in STOPWORDS and x.isalpha(), words)) #added isalpha to check that it contains only letters

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

def get_text_by_uuid(df, uuid):
    return df.loc[df.uuid == uuid].text[0] 

def generate_ngram(text, n):
    ngrams = {}
    #store appearance count of each trigram
    for index in range(0, len(text) + 1 - n):
        ngram = ' '.join(text[index:index+n])
        ngrams.setdefault(ngram, 0) #sets curr ngram to 0 if non-existant
        ngrams[ngram] += 1
    return dict(sorted(ngrams.items(), key=lambda item: item[1])) #return sorted by count

def generate_ngram_by_uuid(df, uuid, n):
    text = get_text_by_uuid(df, uuid)
    return generate_ngram(text, n)

def get_n_most_occuring(dic, n=100):
    sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1])) #sorts in case of additionas post generate_ngram
    return list(sorted_dict)[:n]

<<<<<<< HEAD
# Currently, this uses the n most occuring ngrams to compare
# This could also count the instances in the highest
=======
#Currently, this uses the n most occuring ngrams to compare
#This could also count the instances in the highest
>>>>>>> 33b86ba (OAP 26 Initial trigram processing work)
def get_similarity_score(ngram1, ngram2, n=100):
    n_most_occ_1 = get_n_most_occuring(ngram1, n)
    n_most_occ_2 = get_n_most_occuring(ngram2, n)
    repeated = 0
    for n_gram in n_most_occ_1:
        if n_gram in n_most_occ_2:
            repeated += 1
    return repeated/n
<<<<<<< HEAD

# this treats ngrams1 as primary ngrams, since we want a 
# 100% similarity score if all ngrams match from book 1
# this means that a fragment of a book will get a 100% similarity score
# when compared to it's own book, but not the reverse interaction
def get_similarity_score_by_dict_count(ngrams1, ngrams2):
    repeated = 0
    total = sum(ngrams1.values()) #gets counts from book 1
    for key, ngrams1_value in ngrams1.items():
        repeated += min(ngrams1_value, ngrams2.get(key, 0)) #adds min value, or 0 by default if key not found
    return repeated/total
=======
>>>>>>> 33b86ba (OAP 26 Initial trigram processing work)

def run_ngrams():
    data = get_data()
    # Uncomment to print raw text of first book
    # for item in data:
    #     print(item.get_text_bitstream())
    #     break
    df = make_df(data)
    print(df.shape)
    print(df)
    sample_list = get_text_by_uuid(df, df.iloc[0].uuid)
    print(sample_list[:10])
    sample_ngram_list = generate_ngram_by_uuid(df, df.iloc[0].uuid, 3)
    print(get_n_most_occuring(sample_ngram_list, 2))