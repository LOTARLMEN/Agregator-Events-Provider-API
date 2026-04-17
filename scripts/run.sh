#!/bin/bash
set -e

DB_URL="postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}"

python3 -c "from sqlalchemy import create_engine; engine = create_engine('$DB_URL'); engine.connect().execute('DROP TABLE IF EXISTS alembic_version CASCADE')"

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp head

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000