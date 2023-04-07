# OAPEN Suggestion Engine

## Description
The OAPEN Suggestion Engine will suggest e-books based on other books with similar content. It achieves this using a trigram semantic inferecing algorithm.

## Table of Contents

- [Setup](#setup)
- [Configuration](#configuration)
- [Endpoints](#dependencies)
- [Service Components](#service-components)

## Installation

### 1. Install Docker

This project uses Docker. To run the project, you will need to have Docker installed. You can find instructions for installing Docker [here](https://docs.docker.com/get-docker/). Note that on Linux, if you do not install Docker with Docker Desktop, you will have to install Docker Compose separately, instructions for which can be found [here](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin).

### 2. Install PostgreSQL

The project uses PostgreSQL as a database. You can find instructions for installing PostgreSQL [here](https://www.postgresql.org/download/).
Make sure it is running, and a database is created. Take note of the credentials and name of the database you create, you will need them for the next step.

### 3. Clone the repository

Clone the repository:

```bash
git clone https://github.com/EbookFoundation/oapen-suggestion-service.git
```

And go into the project directory:

```bash
cd oapen-suggestion-service
```

### 4. Configure the environment

And create a file `.env` with the following, replacing `<>` with the described values:

```properties
API_PORT=<Port to serve API on>
WEB_DEMO_PORT=<Port to serve web demo on>
EMBED_SCRIPT_PORT=<Port to serve embed script on>
POSTGRES_HOST=<Hostname of postgres server, will be "localhost" on local installation>
POSTGRES_PORT=<Port postgres is running on, default of 5432 in most cases>
POSTGRES_DB_NAME=<Name of the postgres database, "postgres" works fine here>
POSTGRES_USERNAME=<Username of the postgres user>
POSTGRES_PASSWORD=<Password of the postgres user>
```

> The service **will not run** if this is improperly configured.

### 5. Run the service

Now you can simply start the service with:

```bash
docker compose up
```

You can now connect to the API at `http://localhost:<API_PORT>`

## Configuration

> *More configuration options should go here*

## Endpoints

The API provides access to the following endpoints:

- `http://localhost:3001/api/{handle}`
  - e.g. http://localhost:3001/api/20.400.12657/47581
- `http://localhost:3001/api/{handle}/?threshold={integer}`
  - e.g. http://localhost:3001/api/20.400.12657/47581/?threshold=5
- `http://localhost:3001/api/{handle}/ngrams`
  - e.g. http://localhost:3001/api/20.400.12657/47581/ngrams

## Service Components

This project is a monorepo, with multiple services that work in tandem to provide suggestions: the database, the suggestion engine, the API server, the embed script, and the web demo.

- [Database](#2-install-postgresql)
- [Suggestion Engine](#suggestion-engine)
- [API](#api)
- [Embed Script](#)
- [Web Demo](#)

### Suggestion Engine

This engine is written in Python, and generates the recommendation data for users.
Our suggestion service is centered around the trigram semantic inferencing algorithm. This script should be run as a job on a cron schedule to periodically ingest new texts added to the OAPEN catalog through their API. It populates the database with pre-processed lists of suggestions for each entry in the catalog.

You can find the code for the suggestion engine in `oapen-engine/`, and read more about it in [`oapen-engine/README.md`](oapen-engine/README.md).

### API

This API server serves book recommendations from the database over HTTP in a standard RESTful architecture.

You can find the code for the API in `api/`, and readmore about it in [`api/README.md`](api/README.md).

### Embed Script
> To be added

### Web Demo (Optional)

This is a web-app demo that can be used to query the API engine and see suggested books. This does not have to be maintained if the API is used on another site, but is useful for development and a tech demo.

You can find the code for the web demo in `web/`.

Configuration info for the web demo is in [`web/README.md`](web/README.md).