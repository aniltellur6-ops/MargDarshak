from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.async_database_url, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
