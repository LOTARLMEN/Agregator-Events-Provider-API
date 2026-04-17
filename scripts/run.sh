#!/bin/bash
set -e

DB_URL="postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}"

echo "--- ВЗЛОМ СИСТЕМЫ: Очистка таблицы миграций ---"

uv run python -c "
import asyncio
import asyncpg
async def main():
    try:
        conn = await asyncpg.connect('$DB_URL')
        # Удаляем только таблицу с версиями, данные не трогаем
        await conn.execute('DROP TABLE IF EXISTS alembic_version CASCADE')
        await conn.close()
        print('DONE: Таблица удалена, Alembic больше не видит старую ревизию')
    except Exception as e:
        print(f'ОШИБКА: {e}')
asyncio.run(main())
"

MIGRATIONS_DIR="src/migration/versions"

if [ -z "$(ls -A $MIGRATIONS_DIR/*.py 2>/dev/null)" ]; then
    uv run alembic revision --autogenerate -m "auto_initial_schema"
fi

uv run alembic stamp head

uv run alembic upgrade head

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000