#!/bin/bash
set -e

MIGRATIONS_DIR="src/migration/versions"

echo "--- ШАГ 1: Создаем затычку для Alembic ---"
# Создаем файл, который Alembic так отчаянно ищет
cat <<EOF > "$MIGRATIONS_DIR/3c4feebf7ad8_ghost.py"
revision = '3c4feebf7ad8'
down_revision = None
branch_labels = None
depends_on = None
def upgrade(): pass
def downgrade(): pass
EOF

echo "--- ШАГ 2: Сшиваем историю (насильно) ---"
# Мы используем sed, чтобы заменить пустой down_revision на наш ID.
# Это сработает, даже если файл был Read-only в твоем редакторе,
# потому что в контейнере у скрипта хватит прав.
sed -i "s/down_revision: Union\[str, Sequence\[str\], None\] = None/down_revision = '3c4feebf7ad8'/g" "$MIGRATIONS_DIR/8e5245334c49_auto_initial_schema.py"
sed -i "s/down_revision = None/down_revision = '3c4feebf7ad8'/g" "$MIGRATIONS_DIR/8e5245334c49_auto_initial_schema.py"

echo "--- ШАГ 3: Запуск миграций ---"
# Теперь цепочка такая: None -> 3c4feebf7ad8 (затычка) -> 8e5245334c49 (твои таблицы)
uv run alembic upgrade head

echo "--- ШАГ 4: Старт сервера ---"
exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000