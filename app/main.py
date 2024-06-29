from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from config import settings
from routers import authors, books, users
from surprise import dump

from services import ml_models
from services.database import sessionmanager
from services.docs import convert_openapi_3_1_to_3_0


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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title="", version="0.1.0", openapi_version="3.0.1", routes=app.routes)
    convert_openapi_3_1_to_3_0(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
