import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from src.config.config import setting
from src.presentation.api.lifespan import lifespan
from src.presentation.api.rest.handlers import handlers_mapping
from src.presentation.api.rest.middlewares.metrics_middleware import MetricsMiddleware
from src.presentation.api.rest.router import router

sentry_sdk.init(
    dsn=setting.SENTRY_DSN,
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    traces_sample_rate=1.0,
)

app = FastAPI(lifespan=lifespan, title="Event Aggregator API")

app.add_middleware(MetricsMiddleware)

for exc, handler in handlers_mapping.items():
    app.add_exception_handler(exc, handler)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
