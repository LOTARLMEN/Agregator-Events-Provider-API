#!/bin/bash
set -e

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp base

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000