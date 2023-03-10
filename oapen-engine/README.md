# OAPEN Suggestion Service
## Getting Started
### Running the application
Ensure that you have followed the setup instructions in the top level README, then run:
```
docker-compose up --build
```
### Cleaning the database manually
```
./scripts/clean.sh
```
### Refreshing items + suggestions manually
```
./scripts/refresh.sh
```
## How to remove/filter out bad ngrams
Members of EbookFoundation can create a pull request to edit the stopwords used to filter out bad ngrams, including those that exist in the database:
```
oapen-engine/src/model/stopwords_*.txt
```
This will trigger a regeneration of suggestions on items which contain the new stopwords, filtering them out.

However, if stopwords are *removed* from the filter list (if you wish to allow suggestions to be made on those ngrams from this point forward), the ngrams will not be updated until a full refresh is performed.