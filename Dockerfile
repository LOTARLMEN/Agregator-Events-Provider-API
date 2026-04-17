FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Устанавливаем клиент базы прямо в образ, чтобы не трахать мозг потом
RUN apk add --no-cache postgresql16-client

WORKDIR /app

# Копируем конфиги и ставим зависимости
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Копируем весь проект (включая твой мако-файл и миграции)
COPY . .

# Даем права на запись в папку с миграциями, чтобы алембик не дох
RUN chmod -R 777 /app/src/migration/versions

RUN uv sync --frozen

RUN chmod +x scripts/run.sh

# Используем нормальный шелл
CMD ["/bin/sh", "scripts/run.sh"]