# OAPEN Suggestion Engine

The OAPEN Suggestion Engine will suggest ebooks based on other books with similar content.

## Running the project

The project uses Docker. To run the project, you will need to have Docker installed. You can find instructions for installing Docker [here](https://docs.docker.com/get-docker/).

### 1. Clone the repository

```bash
git clone https://github.com/EbookFoundation/oapen-suggestion-service.git
```

### 2. Install PostgreSQL

The project uses PostgreSQL as a database. You can find instructions for installing PostgreSQL [here](https://www.postgresql.org/download/). 
Make sure it is running, and a database is created.

### 3. Link database to mining engine

Create a `database.ini` file in `oapen-engine/src` with the following:

```
[postgresql]
host=127.0.0.1
database=postgres
user=<username>
password=<your-password>
```

### 4. Link database to API

Edit `config.env` in `api/` with the following:

```
DATABASE_URL="postgres://<username>:<your-password>@127.0.0.1:5432/postgres"
PORT=3001
```

### 5. Run the project

```bash
docker compose up
```

Try connecting to the API at `http://localhost:3001/`.

## Monorepo components

This project is a monorepo, with multiple pieces that can be added or removed as neccessary for deployment.

### [Mining Engine (Core)](/oapen-engine)

This engine is written in Python, and generates the recommendation data for users. 
Our suggestion service is centered around the trigram semantic inferencing algorithm. This script should be run as a job on a cron schedule to periodically ingest new texts added to the OAPEN catalog through their API. It will populate the Database (see Database section) with pre-processed lists of suggestions for each entry in the catalog.

You can find the code for the mining engine in `oapen-engine/`.

**Base dependencies**:
* Python v3.10
* PIP package manager
* `make`

**Automatically-installed dependencies**:
* `nltk` -- Natural language toolkit.
    * Maintained on [GitHub](https://github.com/nltk/nltk) by 300+ contributors. 
    * Most recent update: 8 days ago 
* `requests` -- HTTP request library
    * Maintained on [GitHub](https://github.com/psf/requests) by 600+ conributors, and backed by sponsors.
    * Most recent update: 1 month ago.
* `psycopg2` -- PostgreSQL Database Adapter
    * Maintained on [GitHub](https://github.com/psycopg/psycopg2) by 100+ contributors, and used by 480,000+ packages.
    * Most popular PostgreSQL database adapter for Python
* `pandas` -- data analysis library
    * Maintained by [PYData](https://pandas.pydata.org/) with large amounts of sponsors. 2,700+ contributors.
* `scikit-learn` -- Scikit Learn
    * Maintained by [a large consortium of corporations and open-source developers](https://scikit-learn.org/stable/).


### [API Engine (Core)](/api)

This API server returns a list of recommended books from the database.

You can find the code for the API engine in `api/`.

**Base dependencies**:
* NodeJS 14.x+
* NPM package manager

**Automatically-installed dependencies**:
* `express` - Basic HTTP server
    * Maintained by the [OpenJS foundation](https://expressjs.com/)
    * Largest Node HTTP server
- `pg-promise` -- basic PostgreSQL driver
  - Maintained [on Github](https://github.com/vitaly-t/pg-promise)
- `dotenv` -- loads environment variables from .env
  - Maintained [on Github](https://github.com/motdotla/dotenv)


### [Web Demo (Optional)](/web)

This is a web-app demo that can be used to query the API engine and see suggested books. This does not have to be maintained if the API is used on another site, but is useful for development and a tech demo.

You can find the code for the web demo in `web/`.

**Base dependencies**:
* NodeJS 14.x+
* NPM package manager

**Automatically-installed dependencies**:
* `next` -- Framework for production-driven web apps
    * Maintained by [Vercel](https://vercel.com) and the open source community
* `react` -- Frontend design framework
    * Maintained by [Meta](https://reactjs.org). 
    * Largest frontend web UI library.
    * (Alternative considered: Angular -- however, was recently deprecated by Google)
* `pg` -- basic PostgreSQL driver
    * Maintained [on npm](https://www.npmjs.com/package/pg)
* `typescript` -- Types for JavaScript
    * Maintained by [Microsoft](https://www.typescriptlang.org/) and the open source community.