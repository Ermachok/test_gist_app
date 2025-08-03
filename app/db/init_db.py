from app.db.database import engine, Base
from app.models.coverage_requests import CoverageRequest
import asyncio


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def run_init_db():
    asyncio.run(init_db())
