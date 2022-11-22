# Limit of how many items per collection to import from OAPEN in seed.py
COLLECTION_IMPORT_LIMIT = 50

ITEMS_PER_IMPORT_THREAD = 5

DATA_IMPORT_PRODUCERS = 50

DATA_IMPORT_CONSUMERS = 100

# Size of list of items to process into ngrams per thread
NGRAMS_PER_THREAD = 10

# Number of ngrams that two items need to share in order to be similar
SCORE_THRESHOLD = 5

# How many ngrams to use in item similarity comparision
TOP_K_NGRAMS_COUNT = 30

# Number of threads to generate suggestions
SUGGESTION_THREAD_COUNT = 10
