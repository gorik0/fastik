from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

from src.db.main import init_db
version  = "v1"


@asynccontextmanager
async def life_span(api:FastAPI):
    print(".. starting server ... ")
    await init_db()
    yield
    print(".. finishing  server  ")

app = FastAPI(version=version, title="BOOKS app", description="... Sometrhing about books ... ",lifespan=life_span)
app.include_router(book_router,prefix=f"/api/{version}/books")