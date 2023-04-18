# Suggestion Engine
## Updating/migrating the database
When you make database changes, or add new stopwords, you'll want to completely re-run the harvesting and suggestion creation for the database. Though this happens weekly by default, you have some more immediate options:

To erase & recreate the database _NOW_, you can run:
```bash
docker compose run oapen-engine clean now
```
> *WARNING*: You will lose ALL database data! Reruns are resource-intensive and lengthy, be sure before running this. This _could_ cause unexpected errors if the running service is active, in which case you will need to restart the container.

To erase & recreate the database _on the next run_, you can run:
```bash
docker compose run oapen-engine clean true
```
> *WARNING*: You will lose ALL database data! Reruns are resource-intensive and lengthy, be sure before running this. This is safer than the last command and should not cause any breakage, even if the database is being used by the service actively.

To cancel the operation above, so the database is _not_ erased on the next run, you can run:
```bash
docker compose run oapen-engine clean false
```

### How it works
Those last two operations work by creating/deleting a table called `migrate` in the `oapen_suggestions` schema in the database. When the table exists, the daemon checks for the existence of the table when starting up, and drops & recreates the schema, tables, and types if it exists. It then deletes the table. When the table does not exist, the database is left as-is. You can also manually create the `migrate` table via an SQL query in any database admin tool, and the database will be re-created on the next run.

## Running the engine alone
Ensure that you have followed the [setup instructions](../README.md#installation-server), then run:
```
docker-compose up -d --build
```

## Refreshing items + suggestions manually
```
./scripts/refresh.sh
```

## How to remove/filter out bad ngrams
People with access to the repository can create a pull request to edit the stopwords used to filter out bad trigrams:
```
oapen-engine/src/model/stopwords_*.txt
```
Changes in stopwords will not reflected until the next harvest, which occurs weekly by default.