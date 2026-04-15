import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.presentation.api.rest.handlers import validation_exception_handler

from src.presentation.api.rest.router import router
from src.presentation.api.lifespan import lifespan

app = FastAPI(lifespan=lifespan, title="Event Aggregator API")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
