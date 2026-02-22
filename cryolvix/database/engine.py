from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from cryolvix.config import DATABASE_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=10)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
