#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Running tests..."
    python src/test/data/run_tests.py
    echo "Running app..."
    python src/tasks/daemon.py
elif [ "$1" == "clean" ]; then
    if [ "$2" == "now" ] || [ "$2" == "true" ] || [ "$2" == "false" ]; then
        python src/tasks/clean.py $2
    else
        echo "Invalid arguments for clean. Valid options are 'now', 'true', or 'false'."
        echo "
        Usage: docker compose run oapen-engine clean [now/true/false]
        Options:
        now         Clean the database now. Drops ALL DATA in the database!
        true        Clean the database on the next run of the service. Drops ALL DATA in the database!
        false       Do not clean the database on the next run. Leaves the database as it is."
        exit 1
    fi
else
    echo "Invalid command. Valid commands are 'clean', or you can leave it blank to run the daemon."
    exit 1
fi