import uvicorn
from fastapi import FastAPI
from routers import authors, books, users

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "This is a WIP book recommendation API."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)