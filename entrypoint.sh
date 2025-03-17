#!/bin/sh

uv run main.py

# keep the container running indefinitely
while true; do
  sleep 3600 # Sleep for one hour
done
