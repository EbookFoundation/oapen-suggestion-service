# OAPEN Suggestion API

## About

A basic Node.js + Express api using pg-promise to interface with PostgreSQL and dotenv to read environment variables

## Database Configuration

To use a local connection, create a `database.js` file in `api/src/db` with the following:

```
const config = {
    host: 'localhost',
    port: 5432,
    database: 'my-database-name',
    user: 'user-name',
    password: 'user-password'
};
module.exports = config;
```

e.g.

```
const config = {
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: 'password'
};
module.exports = config;
```

You can also set up local environment variables with that information to connect to the database.

## Running with npm

```
npm ci
npm run seed
npm start
```

Endpoint: /GET http://localhost:3001/api/{item_uuid}

e.g. http://localhost:3001/api/a91a6b7d-874a-4144-b44d-0da647a82acc
