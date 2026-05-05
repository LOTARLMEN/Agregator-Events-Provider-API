FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN apk add --no-cache postgresql16-client

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

RUN chmod -R 777 /app/src/migration/versions

RUN uv sync --frozen

RUN chmod +x scripts/run.sh

CMD ["/bin/sh", "scripts/run.sh"]