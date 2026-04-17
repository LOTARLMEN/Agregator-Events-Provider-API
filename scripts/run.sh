#!/bin/bash
set -e

echo "--- Synchronizing Database Schema State ---"
# Мы сразу штампуем голову (head), это и есть наш файл 8e5245334c49
uv run alembic upgrade head

echo "--- Starting Uvicorn ---"
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000