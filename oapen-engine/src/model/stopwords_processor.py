import os
from functools import reduce

import nltk
from nltk.corpus import stopwords

# This is run as a precaution in case of the error "NLTK stop words not found",
# which makes sure to download the stop words after installing nltk
nltk.download("stopwords")

# add additional custom stopwords to ./custom_lists/ folder and update the reference here
# print working directory
print("Working directory: " + os.getcwd())

current_dir = os.path.realpath(os.path.dirname(__file__))
print("Local script directory: " + current_dir)

custom_lists_folder = current_dir + "/stopwords/"
custom_stopwords_in_use = [
    "broken",
    "dutch",
    "filter",
    "publisher",
]

# For reference on available languages, please reference https://pypi.org/project/stop-words/
enabled_languages = ["english", "german", "dutch"]

# the combined stopwords of all enabled langauges
nltk_stopwords = []
for language in enabled_languages:
    nltk_stopwords += stopwords.words(language)

# get the custom lists
custom_stopwords = []
for custom_list in custom_stopwords_in_use:
    with open(
        custom_lists_folder + custom_list + ".txt", "r"
    ) as file:  # specify folder name
        custom_stopwords += [line.rstrip() for line in file]

# add languages and custom stopwords for final stopwords var
STOPWORDS = set(nltk_stopwords + custom_stopwords)
