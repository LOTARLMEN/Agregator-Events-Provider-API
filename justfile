app_module := "src.main:app"


start:
    uv run uvicorn {{app_module}} --reload --host 127.0.0.1 --port 8000