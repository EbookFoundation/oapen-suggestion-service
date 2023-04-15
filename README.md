# OAPEN Suggestion Service

## Description
The OAPEN Suggestion Service uses natural-language processing to suggest books based on their content similarities. To protect user privacy, we utilize text analysis rather than usage data to provide recommendations. This service is built on the proof-of-concept and paper by Ronald Snijder from the OAPEN Foundation, and you can [read the paper here](https://liberquarterly.eu/article/view/10938).

## Table of Contents
  * [Installation (Server)](#installation--server-)
    + [DigitalOcean Droplet](#digitalocean-droplet)
    + [DigitalOcean Managed Database](#digitalocean-managed-database)
    + [Setup Users & Install Requirements](#setup-users---install-requirements)
    + [Clone & Configure the Project](#clone---configure-the-project)
    + [SSL Certificate](#ssl-certificate)
  * [Running](#running)
  * [Endpoints](#endpoints)
  * [Service Components](#service-components)
    + [Suggestion Engine](#-suggestion-engine--oapen-engine-readmemd-)
    + [API](#-api--api-readmemd-)
    + [Embed Script](#-embed-script--embed-script-readmemd-)
    + [Web Demo](#-web-demo--web-readmemd-)
  * [Updates](#updates)
  * [Local Installation (No Server)](#local-installation--no-server-)

## Installation (Server)

### DigitalOcean Droplet
1. Log in to your DigitalOcean account.
2. Create a new Droplet.
3. Under "Choose an image" select "Marketplace" and search for "Docker". Select "Docker 20.10.21 on Ubuntu 22.04".
4. Choose any size, but the cheapest option will work fine.
5. If you do not have an ssh key, generate one with:
    ```bash
    ssh-keygen -t rsa -b 4096
    ```
    And copy the public key to your clipboard. If you have a key on your computer already, you can use that.
7. Under "Choose Authentication Method" choose "SSH Key" and click "New SSH Key", and in the popup window paste the public key you copied to your clipboard. Make sure it is selected.
8. Give the Droplet a name and click "Create".
9. Open the firewall ports 
    - https://cloud.digitalocean.com/networking/firewalls

### DigitalOcean Managed Database
1. From the DigitalOcean dashboard, click "Databases" > "Create Database".
2. Ideally, select the same region & datacenter as the Droplet you just created, so they can be part of the same VPC network.
3. Choose "PostgreSQL v15".
4. Select any sizing plan, but the cheapest one will suffice.
5. Give the database a name, and click "Create Database Cluster".
6. Once the database is done creating (this can take a few minutes), find the "Connection details" section on the new database's page, you will need them later.

### Setup Users & Install Requirements

1. Log in to the droplet over SSH:
    ```bash
    ssh root@<your-droplet-ip>
    ```
2. Create a new user `oapen` and set a password, adding them to the `sudo` and `docker` groups, then login as the new user:

   ```bash
   useradd -m -G sudo,docker oapen
   passwd oapen
   su -l -s /bin/bash oapen
   ```

3. Install the `docker compose` command:
    ```bash
    sudo apt-get update
    sudo apt-get install docker-compose-plugin
    ```

4. Change the SSH configuration file to disallow root login:

   ```bash
   sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
   ```

5. Allow SSH login with non-root user with the same SSH keys you uploaded to DigitalOcean:

    ```bash
    mkdir -p ~/.ssh
    sudo cp /root/.ssh/authorized_keys ~/.ssh/
    sudo chown -R oapen:oapen ~/.ssh
    sudo chmod 700 ~/.ssh
    sudo chmod 600 ~/.ssh/authorized_keys
    sudo systemctl restart ssh
    ```

6. Create a swapfile to avoid issues with high memory usage:

    ```bash
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    ```

    > Feel free to replace `1G` in the first command with `4G`. Although the service should never use this much memory, extra swap never hurts if you have the disk space to spare. More on swap [here](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-20-04).

7. Restart the droplet to persist all of the changes. From now on, login to the droplet with:

    ```bash
    ssh oapen@<your-droplet-ip>
    ```

### Clone & Configure the Project

1. Clone the repository and cd into the directory it creates:
    ```bash
    git clone https://github.com/EbookFoundation/oapen-suggestion-service.git
    cd oapen-suggestion-service
    ```
    > You can clone this anywhere but in the home directory is easiest.
2. Copy the `.env.template` file to `.env`:
    ```bash
    cp .env.template .env
    ```

3. Using a text editor like `vim` or `nano` configure all of the options in `.env`:
    ```properties
    API_PORT=<Port to serve API on>
    POSTGRES_HOST=<Hostname of postgres server>
    POSTGRES_PORT=<Port postgres is running on>
    POSTGRES_DB_NAME=<Name of the postgres database>
    POSTGRES_USERNAME=<Username of the postgres user>
    POSTGRES_PASSWORD=<Password of the postgres user>
    POSTGRES_SSLMODE=<'require' when using a managed database>
    ```

    > Postgres credentials can be found in the "Connection details" section of the managed database

4. Open the `docker-compose.yml` file and find the line:
    ```dockerfile
    - RUN_CLEAN=1
    ```
    This is set to `1` by default, which causes the database to be ***COMPLETELY*** deleted and the types recreated each time the server restarts. It is important to have this set to `1` only on the _first run of the application_, or after making changes that affect the structure of the database. As soon as you run the application with the following command, you should change the line to:
    ```dockerfile
    - RUN_CLEAN=0
    ```
    To prevent this behavior.

### SSL Certificate

 > TODO: add documentation


## Running

You can start the services by running the following command in the directory where you cloned the repo:
```bash
docker compose up -d
```
The API will be running on `https://<your-ip>:<API_PORT>`.

> *NOTE*: The `-d` flag runs the services in the background, so you can safely exit the session and the services will continue to run.

You can stop the services with:
```bash
docker compose down
```

You can view the logs with:
```bash
docker compose logs -f
```
> You can dump them with `docker compose logs > some_file.txt`

To view the logs for just a specific service component - for example the mining enginge - use:
```bash
docker logs -f oapen-suggestion-service-oapen-engine-1
```

## Endpoints

The API provides access to the following endpoints:

- `http://localhost:3001/api/{handle}`
  - e.g. http://localhost:3001/api/20.400.12657/47581
- `http://localhost:3001/api/{handle}/?threshold={integer}`
  - e.g. http://localhost:3001/api/20.400.12657/47581/?threshold=5
- `http://localhost:3001/api/{handle}/ngrams`
  - e.g. http://localhost:3001/api/20.400.12657/47581/ngrams

## Service Components

This project is a monorepo, with multiple services that work in tandem to provide suggestions:

- [Database](#2-install-postgresql)
- [Suggestion Engine](#suggestion-engine)
- [API](#api)
- [Embed Script](#embed-script)
- [Web Demo](#web-demo-optional)

### [Suggestion Engine](oapen-engine/README.md)

This engine is written in Python, and generates the recommendation data for users.
Our suggestion service is centered around the trigram semantic inferencing algorithm. This script should be run as a job on a cron schedule to periodically ingest new texts added to the OAPEN catalog through their API. It populates the database with pre-processed lists of suggestions for each entry in the catalog.

You can find the code for the suggestion engine in `oapen-engine/`, and read more about it in [`oapen-engine/README.md`](oapen-engine/README.md).

### [API](api/README.md)

This API server serves book recommendations from the database over HTTP in a standard RESTful architecture.

You can find the code for the API in `api/`, and readmore about it in [`api/README.md`](api/README.md).

### [Embed Script](embed-script/README.md)

The embed script is a drop-in snippet of HTML, CSS, and JavaScript that can be added to the [library.oapen.org](https://library.oapen.org/) site, and adds book recommendation functionality to the sidebar of each book page.

You can find the code for the embed script in `embed-script/`, and read more about it in [`embed-script/README.md`](embed-script/README.md).

### [Web Demo](web/README.md)

This is a web-app demo that can be used to query the API engine and see suggested books. This does not have to be maintained if the API is used on another site, but is useful for development and a tech demo.

You can find the code for the web demo in `web/`.

Configuration info for the web demo is in [`web/README.md`](web/README.md).

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

## Updates
> TODO: add documentation

## Local Installation (No Server)

1. **Install Docker**

    This project uses Docker. Instructions for installing Docker [here](https://docs.docker.com/get-docker/). Note that if you do not install Docker with Docker Desktop (which is recommended) you will have to install Docker Compose separately Instructions for that [here](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin).

2. **Install PostgreSQL**
    
    You can find instructions for installing PostgreSQL on your machine [here](https://www.postgresql.org/download/).

    Or you can create a PostgreSQL server with Docker:
    
    ```bash
    docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgrespw postgres
    ```
    
    > The username and database name will both be `postgres` and the password will be `postgrespw`. You can connect via the hostname `host.docker.internal` over port `5432`.

3. **Clone and configure the project**

    - Clone the repo and go into its directory:

        ```bash
        git clone https://github.com/EbookFoundation/oapen-suggestion-service.git
        cd oapen-suggestion-service
        ```
    - Copy the `.env.template` file to `.env`:
        ```bash
        cp .env.template .env
        ```

    - Using a text editor like `vim` or `nano` configure all of the options in `.env`:
        ```properties
        API_PORT=<Port to serve API on>
        POSTGRES_HOST=<Hostname of postgres server>
        POSTGRES_PORT=<Port postgres is running on>
        POSTGRES_DB_NAME=<Name of the postgres database>
        POSTGRES_USERNAME=<Username of the postgres user>
        POSTGRES_PASSWORD=<Password of the postgres user>
        POSTGRES_SSLMODE=<'allow' for a local installation>
        ```
    - Open the `docker-compose.yml` file and find the line:
        ```dockerfile
        - RUN_CLEAN=1
        ```
        This is set to `1` by default, which causes the database to be ***COMPLETELY*** deleted and the types recreated each time the server restarts. It is important to have this set to `1` only on the _first run of the application_, or after making changes that affect the structure of the database. As soon as you run the application with the following command, you should change the line to:
        ```dockerfile
        - RUN_CLEAN=0
        ```
        To prevent this behavior.
4. See [Running](#running)