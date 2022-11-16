# OAPEN Suggestion Service
## Getting Started
### Database Configuration (Local)
Create a `database.ini` file in `oapen-engine/src` with the following:
```
[postgresql]
host=localhost
database=postgres
user=<username>
password=<your-password>
```
### Environment setup
```
cd oapen-engine
make setup-env
```
### Seeding the database
```
make clean_db
make seed_db
```
### Running ngrams
```
make run
```
## How to deactivate virtual environment
While the virtual environment is running, type:
```
deactivate
```
## How to remove/filter out bad ngrams
Members of EbookFoundation can create a pull request to edit the stopwords used to filter out bad trigrams:
```
oapen-engine/src/model/stopwords_*.txt
```
This also can be done to remove a malformed trigram already in the database (during the next run)