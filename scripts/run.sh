#!/bin/sh

echo "Current directory: $(pwd)"
echo "Checking for alembic.ini..."
ls -la /app/alembic.ini

# Запускаем миграции, ПРИНУДИТЕЛЬНО указав путь к конфигу
alembic -c /app/alembic.ini upgrade head

# Если миграции упадут, эта строка не даст контейнеру закрыться
if [ $? -ne 0 ]; then
    echo "Migrations failed, but I will stay alive for your debug..."
    sleep infinity
fi

# Если всё ок, запускаем сервер
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000