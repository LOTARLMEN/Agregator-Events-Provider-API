#!/bin/bash
set -e

DB_URL="postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}"

echo "--- ВЗЛОМ СИСТЕМЫ: Очистка таблицы миграций ---"

HOME=/tmp uv run python -c "
import asyncio
import asyncpg
import sys

async def main():
    try:
        # Прямое подключение без лишних проверок
        conn = await asyncpg.connect('$DB_URL')
        await conn.execute('DROP TABLE IF EXISTS alembic_version CASCADE')
        await conn.close()
        print('SUCCESS: Таблица alembic_version удалена.')
    except Exception as e:
        print(f'КРИТИЧЕСКАЯ ОШИБКА: {e}')
        # Не выходим с ошибкой, чтобы скрипт шел дальше,
        # но мы увидим лог

asyncio.run(main())
"

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp head

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000