# OAPEN Suggestion Service
## Database Configuration (Local)
Create a `database.ini` file in `oapen-engine/src` with the following:
```
[postgresql]
host=localhost
database=postgres
user=<username>
password=<your-password>
```
## Running with Pipenv
```
pipenv install
pipenv shell
cd src
python main.py
```
## Deactivate virtual environment
While the virtual environment is running, type:
```
deactivate
```
