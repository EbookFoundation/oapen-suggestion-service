# Limit of how many items per collection to import from OAPEN in seed.py
COLLECTION_IMPORT_LIMIT = 10

ITEMS_PER_IMPORT_THREAD = 25

# Max thread count for data ingest
IO_MAX_WORKERS = 10

# Size of list of items to process into ngrams per process
NGRAMS_PER_PROCESS = 25
NGRAMS_PER_INSERT = 100


# Number of ngrams that two items need to share in order to be similar
SCORE_THRESHOLD = 5

# How many ngrams to use in item similarity comparision
TOP_K_NGRAMS_COUNT = 30

# Number of threads to generate suggestions
SUGGESTIONS_MAX_WORKERS = 100
SUGGESTIONS_MAX_ITEMS = 10


# Update items that were modifed since X days ago
UPDATE_DAYS_BEFORE = 30
REFRESH_IMPORT_LIMIT = 50
