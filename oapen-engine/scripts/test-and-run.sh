#!/bin/sh

# exit when any command fails
set -e

echo "Running tests..." && \
python src/test/data/run_tests.py && \
echo "Running app" && \
python src/tasks/daemon.py