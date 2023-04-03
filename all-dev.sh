#!/bin/bash

# TODO add mining engine
echo "Mining engine is not yet supported, running web servers"

export NODE_ENV='development'

./run-api.sh &
./run-web.sh