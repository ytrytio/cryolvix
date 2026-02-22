from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_or_create(self, user_id: int, name: str, username: str | None = None) -> User:
        user = await self.get_by_id(user_id)
        
        if not user:
            user = User(
                id=user_id,
                name=name,
                username=username,
                created=int(datetime.now().timestamp()),
                money=5000,
                cryocoins=0
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        else:
            if user.name != name or user.username != username:
                user.name = name
                user.username = username
                await self.session.commit()
                await self.session.refresh(user)
                
        return user

    async def update(self, user_id: int, **kwargs):
        query = update(User).where(User.id == user_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def get_with_gpus(self, user_id: int):
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.gpus))
        )
        return result.scalar_one_or_none()
