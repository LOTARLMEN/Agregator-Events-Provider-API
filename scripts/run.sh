#!/bin/bash
set -e

# 1. Помечаем призрак (на всякий случай, если база чистая)
uv run alembic stamp 3c4feebf7ad8

# 2. Помечаем твою основную миграцию как ВЫПОЛНЕННУЮ.
# Мы не используем upgrade, чтобы он не пытался снова создать таблицу "places".
# Stamp просто запишет ID 8e5245334c49 в таблицу alembic_version.
echo "Stamping main migration as already done..."
uv run alembic stamp 8e5245334c49

# 3. Запуск сервера
echo "Starting app..."
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000