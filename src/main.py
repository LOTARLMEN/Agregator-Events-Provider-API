import uvicorn
from fastapi import FastAPI

from src.presentation.api.rest.handlers import handlers_mapping

from src.presentation.api.rest.router import router
from src.presentation.api.lifespan import lifespan

app = FastAPI(lifespan=lifespan, title="Event Aggregator API")


for exc, handler in handlers_mapping.items():
    app.add_exception_handler(exc, handler)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
