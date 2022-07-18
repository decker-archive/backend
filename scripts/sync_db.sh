#!/bin/bash

cd petabyte
poetry install
poetry run python petabyte/connector.py
echo "Finished Syncing Database"
