#!/bin/bash

rm ./nginx/nginx.conf.template
cp ./nginx/nginx.conf ./nginx/nginx.conf.template
docker compose up --build -d nginx