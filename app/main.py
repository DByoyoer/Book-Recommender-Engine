from fastapi import FastAPI
from routers import authors, books, users

app = FastAPI()

app.include_router(books.router)
@app.get("/")
async def root():
    return {"message": "This is a WIP book recommendation API."}