ITEMS_PER_IMPORT_THREAD = 25

# Max thread count for data ingest
IO_MAX_WORKERS = 10

# Delay for submitting new API call thread
HARVEST_THREAD_SPAWN_DELAY = 2

# Size of list of items to process into ngrams per process
NGRAMS_PER_INSERT = 100

# Minimum number of ngrams that two items need to share in order to be similar
SCORE_THRESHOLD = 1

# How many ngrams to use in item similarity comparision
TOP_K_NGRAMS_COUNT = 30

# Number of threads to generate suggestions
SUGGESTIONS_MAX_WORKERS = 250
SUGGESTIONS_MAX_ITEMS = 25

# Update items that were modifed since X days ago
UPDATE_DAYS_BEFORE = 30
REFRESH_IMPORT_LIMIT = 50
