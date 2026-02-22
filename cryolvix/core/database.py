from asyncio import run as aiorun
from cryolvix.database.engine import engine
from cryolvix.database.models.base import Base

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    aiorun(init())
