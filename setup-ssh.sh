#!/bin/bash

rm ./nginx/nginx.conf.template
cp ./nginx/nginx-challenge.conf ./nginx/nginx.conf.template
docker compose up --build -d nginx certbot