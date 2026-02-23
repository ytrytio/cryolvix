from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User

class GlobalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_top_by_balance(self) -> list[User]:
        query = select(User).order_by(User.money.desc()).limit(10)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_top_by_cryocoins(self) -> list[User]:
        query = select(User).order_by(User.cryocoins.desc()).limit(10)
        result = await self.session.execute(query)
        return list(result.scalars().all())
