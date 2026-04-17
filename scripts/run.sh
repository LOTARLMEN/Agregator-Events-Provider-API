#!/bin/bash
set -e

# 1. Даем себе права на запись в папку миграций.
# Без этого 'alembic revision' упадет с Permission denied.
chmod -R 777 src/migration/versions

echo "--- ГЕНЕРИРУЕМ МИГРАЦИЮ ВНУТРИ КОНТЕЙНЕРА ---"
# Генерируем файл миграции, который сравнит модели с базой и создаст недостающее (типы, таблицы)
uv run alembic revision --autogenerate -m "auto_fix_from_k8s"

echo "--- ПРИМЕНЯЕМ ---"
uv run alembic upgrade head

echo "--- ЗАПУСК ПРИЛОЖЕНИЯ ---"
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000