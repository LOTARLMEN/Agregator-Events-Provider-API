#!/bin/bash
set -e

MIGRATIONS_DIR="src/migration/versions"

# 1. Мы просто связываем твою основную миграцию с призраком прямо перед запуском.
# Это "сшьет" их в одну линию: 3c4 -> 8e5.
sed -i "s/down_revision: Union\[str, Sequence\[str\], None\] = None/down_revision = '3c4feebf7ad8'/g" $MIGRATIONS_DIR/8e5245334c49_auto_initial_schema.py
sed -i "s/down_revision = None/down_revision = '3c4feebf7ad8'/g" $MIGRATIONS_DIR/8e5245334c49_auto_initial_schema.py

# Но в самом файле призрака down_revision должен остаться None!
# Исправляем его обратно, если sed зацепил лишнего.
sed -i "s/down_revision = '3c4feebf7ad8'/down_revision = None/g" $MIGRATIONS_DIR/*3c4feebf7ad8*.py

# 2. Просто запускаем апгрейд.
echo "Applying migrations..."
uv run alembic upgrade head

echo "Starting server..."
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000