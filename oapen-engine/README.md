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
Members of EbookFoundation can create a pull request to edit the stopwords used to filter out bad trigrams:
```
oapen-engine/src/model/stopwords_*.txt
```
This also can be done to remove a malformed trigram already in the database (during the next run)