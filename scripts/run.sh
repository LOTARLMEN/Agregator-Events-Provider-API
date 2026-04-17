#!/bin/bash
# Убираем set -e, чтобы скрипт не падал, если Alembic ругнется
set +e

echo "--- Trying to sync migrations (safe mode) ---"
# Пробуем накатить, но если упадет (например, из-за таблиц) — идем дальше
uv run alembic upgrade head

echo "--- Starting Uvicorn (Even if migrations failed) ---"
# Теперь Uvicorn запустится в любом случае, Под станет Ready (1/1)
# и ты сможешь сделать kubectl exec -it ... -- sh
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000