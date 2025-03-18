#!/bin/sh

echo "Syncing dependencies with uv"
uv sync

echo "Activating virtual environment"
source .venv/bin/activate

echo "Running main.py with python"
python -u main.py

echo "main.py finished"

while true; do
  sleep 3600
done
