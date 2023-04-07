# OAPEN Suggestion API
## Configuration

You can specify the port requests will be served on with the `API_PORT` variable. The default value is `3001`.

Follow the [setup instructions](https://github.com/EbookFoundation/oapen-suggestion-service#setup) to ensure the database environment variables are set.

## Endpoints

- `Endpoint: /GET http://localhost:3001/api/{handle}`

  - e.g. http://localhost:3001/api/20.400.12657/47581

- `Endpoint: /GET http://localhost:3001/api/{handle}/?threshold={integer}`

  - e.g. http://localhost:3001/api/20.400.12657/47581/?threshold=5

- `Endpoint: /GET http://localhost:3001/api/{handle}/ngrams`

  - e.g. http://localhost:3001/api/20.400.12657/47581/ngrams


