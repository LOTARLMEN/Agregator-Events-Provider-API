#!/bin/bash
set -e

# 1. Сначала "проглатываем" призрака.
# Мы явно говорим: пометь версию 3c4feebf7ad8 как выполненную.
# Это не требует прав на запись в файлы миграций.
echo "Stamping ghost revision..."
uv run alembic stamp 3c4feebf7ad8

# 2. Теперь накатываем твою основную миграцию.
# Так как в базе уже сидит 3c4..., Alembic увидит вторую "голову" 8e5245334c49.
# Мы явно указываем её ID, чтобы он не путался в "Multiple heads".
echo "Applying main migration..."
uv run alembic upgrade 8e5245334c49

# 3. Запуск сервера
echo "Starting app..."
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000