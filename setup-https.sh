#!/bin/bash

docker compose stop nginx certbot
docker compose rm -f nginx certbot
docker compose --file docker-compose-https.yml up -d
docker wait certbot
docker compose logs certbot
docker compose --file docker-compose-https.yml down
docker compose --file docker-compose-https.yml rm -f nginx certbot