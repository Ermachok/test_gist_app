from app.db.database import AsyncSessionLocal


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
