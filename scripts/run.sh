#!/bin/sh
set -e

echo "--- Waiting for Database to be ready ---"
# Используем переменные из композа: DB_USER, DB_PASS, DB_NAME и имя сервиса 'db'
export PGPASSWORD=$DB_PASS
until psql -h db -U $DB_USER -d $DB_NAME -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "--- Wiping Database (The Nuclear Option) ---"
psql -h db -U $DB_USER -d $DB_NAME -c "DROP TABLE IF EXISTS tickets, events, places, alembic_version CASCADE;"
psql -h db -U $DB_USER -d $DB_NAME -c "DROP TYPE IF EXISTS eventstatus;"

echo "--- Running Fresh Migrations ---"
# Теперь база пустая, алембик создаст всё сам, включая Enum
uv run alembic upgrade head

echo "--- Starting Application ---"
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000