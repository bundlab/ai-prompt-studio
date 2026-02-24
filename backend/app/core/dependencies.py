from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=StaticPool)
async def get_db():
    async with AsyncSession(engine) as session:
        yield session
