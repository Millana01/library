import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.authors.router import router as author_router
from src.books.router import router as book_router
from src.users.router import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(author_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
