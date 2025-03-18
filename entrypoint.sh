#!/bin/sh
echo "uv syncing"
uv sync
echo "uv running"
uv run main.py
