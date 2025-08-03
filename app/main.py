from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import coverage


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Cell coverage API", lifespan=lifespan)

app.include_router(coverage.router)


@app.get("/")
async def root():
    return {"message": "Cell coverage API is running"}
