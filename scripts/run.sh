#!/bin/bash
set -e

uv run alembic -c src/migration/alembic.ini  -x db_url="postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}" \
  run_sql "DROP TABLE IF EXISTS alembic_version CASCADE;" || echo "SQL failed, but moving on..."

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp head

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000