# OAPEN Suggestion Engine

The OAPEN Suggestion Engine will suggest ebooks based on other books with similar content.

## Setup

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

### 4. Configure Environment

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

### 5. Run the project

Now you can simply start the service with:

```bash
docker compose up
```

You can now connect to the API at `http://localhost:<API_PORT>`

## Endpoints

The API provides access to the following endpoints:

- `http://localhost:3001/api/{handle}`
  - e.g. http://localhost:3001/api/20.400.12657/47581
- `http://localhost:3001/api/{handle}/?threshold={integer}`
  - e.g. http://localhost:3001/api/20.400.12657/47581/?threshold=5
- `http://localhost:3001/api/{handle}/ngrams`
  - e.g. http://localhost:3001/api/20.400.12657/47581/ngrams

## Monorepo components

This project is a monorepo, with multiple pieces that can be added or removed as neccessary for deployment.

### [Mining Engine (Core)](/oapen-engine)

This engine is written in Python, and generates the recommendation data for users.
Our suggestion service is centered around the trigram semantic inferencing algorithm. This script should be run as a job on a cron schedule to periodically ingest new texts added to the OAPEN catalog through their API. It will populate the Database (see Database section) with pre-processed lists of suggestions for each entry in the catalog.

You can find the code for the mining engine in `oapen-engine/`.

Information about running the mining engine is in [`oapen-engine/README.md`](oapen-engine/README.md).

**Base dependencies**:

- Python v3.10
- PIP package manager
- `make`

**Automatically-installed dependencies**:

- `nltk` -- Natural language toolkit.
  - Maintained on [GitHub](https://github.com/nltk/nltk) by 300+ contributors.
  - Most recent update: 8 days ago
- `requests` -- HTTP request library
  - Maintained on [GitHub](https://github.com/psf/requests) by 600+ conributors, and backed by sponsors.
  - Most recent update: 1 month ago.
- `psycopg2` -- PostgreSQL Database Adapter
  - Maintained on [GitHub](https://github.com/psycopg/psycopg2) by 100+ contributors, and used by 480,000+ packages.
  - Most popular PostgreSQL database adapter for Python
- `pandas` -- data analysis library
  - Maintained by [PYData](https://pandas.pydata.org/) with large amounts of sponsors. 2,700+ contributors.
- `scikit-learn` -- Scikit Learn
  - Maintained by [a large consortium of corporations and open-source developers](https://scikit-learn.org/stable/).

### [API Engine (Core)](/api)

This API server returns a list of recommended books from the database.

You can find the code for the API engine in `api/`.

Configuration info for the API engine is in [`api/README.md`](api/README.md).

**Base dependencies**:

- NodeJS 14.x+
- NPM package manager

**Automatically-installed dependencies**:

- `express` - Basic HTTP server
  - Maintained by the [OpenJS foundation](https://expressjs.com/)
  - Largest Node HTTP server

* `pg-promise` -- basic PostgreSQL driver
  - Maintained [on Github](https://github.com/vitaly-t/pg-promise)
* `dotenv` -- loads environment variables from .env
  - Maintained [on Github](https://github.com/motdotla/dotenv)

### [Web Demo (Optional)](/web)

This is a web-app demo that can be used to query the API engine and see suggested books. This does not have to be maintained if the API is used on another site, but is useful for development and a tech demo.

You can find the code for the web demo in `web/`.

Configuration info for the web demo is in [`web/README.md`](web/README.md).

**Base dependencies**:

- NodeJS 14.x+
- NPM package manager

**Automatically-installed dependencies**:

- `next` -- Framework for production-driven web apps
  - Maintained by [Vercel](https://vercel.com) and the open source community
- `react` -- Frontend design framework
  - Maintained by [Meta](https://reactjs.org).
  - Largest frontend web UI library.
  - (Alternative considered: Angular -- however, was recently deprecated by Google)
- `pg` -- basic PostgreSQL driver
  - Maintained [on npm](https://www.npmjs.com/package/pg)
- `typescript` -- Types for JavaScript
  - Maintained by [Microsoft](https://www.typescriptlang.org/) and the open source community.
