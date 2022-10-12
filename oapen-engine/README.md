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
