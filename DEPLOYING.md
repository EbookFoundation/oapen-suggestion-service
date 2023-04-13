# Deployment Guide

## Prerequisites

Before we begin, you should already have the following:

- A DigitalOcean account.
- `ssh` installed locally on your computer, comes pre-installed with most operating systems.

## Step 1: Create SSH/find keys

1. **Check for existing SSH keypair:** 
To check if an SSH keypair already exists on your machine, open a terminal and type the following command:
    
    ```
    ls ~/.ssh
    ```
    
    If there is an existing keypair, you will see output containing something like this:
    
    ```
    /home/username/.ssh/id_rsa  /home/username/.ssh/id_rsa.pub
    ```
    
    If there is no output, then you do not have an existing keypair.

2. **Generate a new SSH keypair:**
If you do not have an existing keypair, you can generate a new one using the following command:
    
    ```
    ssh-keygen -t rsa -b 4096
    ```
    
    This command generates a new RSA keypair with a key length of 4096 bits.

    You can add an optional passphrase, which adds an extra layer of security, as anyone who gains access to your key will also need to know the passphrase to use it. If you want to add a passphrase, you will be prompted to enter it twice.

3. **Copy the public key to the clipboard:**
Copy and paste the contents of the .pub file, typically id_rsa.pub, by using the cat command to output the key to the terminal:
    
    ```
    cat ~/.ssh/id_rsa.pub
    ```


## Step 2: Create a new DigitalOcean droplet

1. Log in to your DigitalOcean account.
2. Click the "Create" button and select "Droplets".
3. Choose a region & datacenter closest to your majority audience.
4. Under "Choose an image" select "Marketplace" and search for "Docker". There should be an image option named "Docker 20.10.21 on Ubuntu 22.04", select that image:
![Image](https://i.imgur.com/jibKdDq.png)
5. Choose any options under "Choose Size", but the cheapest option as pictured should more than suffice:
![Sizing options](https://i.imgur.com/ZBzsHUV.png)
6. Under "Choose Authentication Method" choose "SSH Key" and click "New SSH Key", and in the popup window paste the public key you copied to your clipboard earlier.
7. Give the Droplet a name, and click "Create Droplet".
8. Once the Droplet is done spinning up, copy the IPv4 address.

## Step 3: Create a non-root user with sudo privileges

1. Log in to your droplet as the root user over SSH:

   ```
   ssh root@<your-droplet-ip>
   ```

2. Create a new user and set a password, then add them to the `sudo` and `docker` groups:

   ```
   adduser --create-home <username>
   passwd <username>
   usermod -aG sudo,docker <username>
   ```

4. Edit the SSH configuration file to disallow root login:

   ```
   nano /etc/ssh/sshd_config
   ```

5. Find the line that reads `PermitRootLogin yes` and change it to `PermitRootLogin no`. Save and exit the file.
7. Allow SSH login with non-root user with the same SSH keys you uploaded:

    ```
    su - <username>
    mkdir -p ~/.ssh
    sudo cp /root/.ssh/authorized_keys ~/.ssh/
    sudo chown -R $USER:$USER ~/.ssh
    sudo chmod 700 ~/.ssh
    sudo chmod 600 ~/.ssh/authorized_keys
    ```

8. Restart the SSH service to enforce the changes you made:

   ```
   sudo systemctl restart ssh
   ```

## Step 4: Setup a new DigitalOcean managed database

1. From the DigitalOcean dashboard, click on the "Databases" tab.
2. Click "Create Database".
3. For the region, it is ideal to select the same region & datacenter as the Droplet you just created, so they can be part of the same VPC network.
4. Choose "PostgreSQL" and select "v15" for the version.
5. Under "Choose a database configuration", you may select any plan, though the smallest size as pictured should more than suffice: ![DB Sizing options](https://i.ibb.co/0GxMzvX/Screenshot-2023-04-10-at-8-23-26-AM.png)
6. Give the database a name, and click "Create Database Cluster".
7. Once the database is done creating (this can take a few minutes), find the "Connection details" section on the Database Cluster's page: ![Connection details](https://i.ibb.co/cg8LtPG/Screenshot-2023-04-10-at-9-01-22-AM.png)
    You will need these for the next step.

## Step 5: Clone & Configure the Repository

1. Login to the droplet (not the database) with the non-root user you created:
    ```
    ssh <username>@<droplet-ip>
    ```
2. Install the Docker Compose plugin:
    ```bash
    sudo apt-get update
    sudo apt-get install docker-compose-plugin
2. Clone the repository and go into the directory it creates:
    ```
    git clone https://github.com/EbookFoundation/oapen-suggestion-service.git
    cd oapen-suggestion-service
    ```
4. Now, edit the `.env` file using the editor of your choice, `nano` or `vim`, you will need to configure all of the options for the application to work properly:
    ```properties
    API_PORT=<Port to serve API on>
    POSTGRES_HOST=<Hostname of postgres server>
    POSTGRES_PORT=<Port postgres is running on>
    POSTGRES_DB_NAME=<Name of the postgres database>
    POSTGRES_USERNAME=<Username of the postgres user>
    POSTGRES_PASSWORD=<Password of the postgres user>
    ```
5. **NOTE:** Open the `docker-compose.yml` file and find the line:
    ```dockerfile
    - RUN_CLEAN=1
    ```
    This is set to `1` by default, which causes the database to be ***COMPLETELY*** deleted and the types recreated each time the server restarts. It is important to have this set to `1` only on the _first run of the application_, or after making changes that affect the structure of the database. As soon as you run the application with the following command, you should change the line to:
    ```dockerfile
    - RUN_CLEAN=0
    ```
    To prevent this behavior.

## Start & Stop the Service
You can start the services from the server by running:
```bash
docker compose up -d
```
And you can stop the services with:
```bash
docker compose down
```