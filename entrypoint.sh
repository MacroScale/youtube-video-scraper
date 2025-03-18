#!/bin/sh
echo "uv syncing"
uv sync
echo "uv running"
uv run main.py

echo "now sleeping"
while true; do
  sleep 3600
done
