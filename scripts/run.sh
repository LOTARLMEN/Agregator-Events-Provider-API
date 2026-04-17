#!/bin/bash
set -e

DB_URL="postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}"
uv run python -c "
from sqlalchemy import create_engine, text
try:
    engine = create_engine('$DB_URL')
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
        conn.commit()
    print('Таблица alembic_version успешно удалена')
except Exception as e:
    print(f'Ошибка при удалении таблицы: {e}')
"

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp head

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000