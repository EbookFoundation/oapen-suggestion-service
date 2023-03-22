# OAPEN Suggestion API

## About

A basic Node.js + Express api using pg-promise to interface with PostgreSQL and dotenv to read environment variables

## Database Configuration

To configure the database connection, create a file called `config.env` in `api/` with the contents

```
DATABASE_URL="postgres://username:password@host:port/database"
PORT=PORT_NUMBER
```

e.g.

```
DATABASE_URL="postgres://postgres:password@localhost:5432/postgres"
PORT=3001
```

To populate the database with seed data, run `make setup-env` from `oapen-engine/`

## Running with npm

```
npm ci
npm start
```

## Endpoints

- `Endpoint: /GET http://localhost:3001/api/{handle}`

  - e.g. http://localhost:3001/api/20.400.12657/47581

- `Endpoint: /GET http://localhost:3001/api/{handle}/?threshold={integer}`

  - e.g. http://localhost:3001/api/20.400.12657/47581/?threshold=5

- `Endpoint: /GET http://localhost:3001/api/{handle}/ngrams`

  - e.g. http://localhost:3001/api/20.400.12657/47581/ngrams


