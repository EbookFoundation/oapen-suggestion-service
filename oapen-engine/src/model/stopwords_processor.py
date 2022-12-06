import nltk
from nltk.corpus import stopwords
from functools import reduce

# This is run as a precaution in case of the error "NLTK stop words not found",
# which makes sure to download the stop words after installing nltk
nltk.download("stopwords")

# add additional custom stopwords to ./stopwords/ folder and update the reference here
custom_stopwords_in_use = [
    "broken",
    "dutch",
    "filter",
    "publisher",
]

# For reference on available languages, please reference https://pypi.org/project/stop-words/
enabled_languages = [
    "english",
    "german",
    "dutch"
]

#the combined stopwords of all enabled langauges
nltk_stopwords = reduce(lambda curr_downloaded_lang_list, next_lang: curr_downloaded_lang_list + stopwords.words(next_lang), enabled_languages) 

for stopword_file in custom_stopwords_in_use:
    with open(p, "r") as f:
        oapen_stopwords += [line.rstrip() for line in f]



STOPWORDS = (
    stopwords.words("english")
    + stopwords.words("german")
    + stopwords.words("dutch")
    + oapen_stopwords
)

#original
# STOPWORDS = (
#     stopwords.words("english")
#     + stopwords.words("german")
#     + stopwords.words("dutch")
#     + oapen_stopwords.stopwords_dutch_extra
#     + oapen_stopwords.stopwords_filter
#     + oapen_stopwords.stopwords_publisher
# )

