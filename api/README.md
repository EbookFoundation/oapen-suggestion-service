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

## Running with npm

```
npm ci
npm run clean
npm start
```

Endpoint: /GET http://localhost:3001/api/{item_uuid}

e.g. http://localhost:3001/api/a91a6b7d-874a-4144-b44d-0da647a82acc

To populate the database with seed data, run `make setup-env` from `oapen-engine/`
