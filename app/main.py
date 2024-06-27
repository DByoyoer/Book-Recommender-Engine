from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config import settings
from routers import authors, books, users
from surprise import dump

from services import ml_models
from services.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    _, ml_models["svd"] = dump.load("data/svd_model.dump")
    yield
    if sessionmanager.engine_exists():
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.api_name)

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "This is a WIP book recommendation API."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
