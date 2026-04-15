import uvicorn
from fastapi import FastAPI
from src.presentation.api.rest.router import router
from src.presentation.api.lifespan import lifespan

app = FastAPI(lifespan=lifespan, title="Event Aggregator API")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
