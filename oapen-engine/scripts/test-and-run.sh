#!/bin/sh

echo "Running tests..." && \
python src/test/data/run_tests.py && \
echo "Running app" && \
python src/tasks/daemon.py