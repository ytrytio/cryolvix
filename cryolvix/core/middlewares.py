from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message, ReactionTypeEmoji
from aiogram.utils.i18n import gettext as i18n

from sqlalchemy.ext.asyncio import async_sessionmaker
from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict, Optional
from random import choice

from cryolvix.database.repositories import UserRepository, GPURepository, ProductRepository, GlobalRepository
from cryolvix.core.userdata import UserData

class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_from_event: Optional[Any] = data.get("event_from_user")

        async with self.session_pool() as session:
            data["session"] = session
            
            gpu_repo = GPURepository(session)
            product_repo = ProductRepository(session)
            user_repo = UserRepository(session)
            global_repo = GlobalRepository(session)
            
            data["gpu_repo"] = gpu_repo
            data["product_repo"] = product_repo
            data["user_repo"] = user_repo
            data["global_repo"] = global_repo

            if user_from_event and not user_from_event.is_bot:
                user_data = await UserData.create_or_load(user_from_event, user_repo)
                await user_data.check_license()
                data["user"] = user_data

            return await handler(event, data)


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: float = 1) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = getattr(event, "from_user", None)
        
        if not user: return await handler(event, data)

        user_id = user.id

        if user_id in self.limit:
            if isinstance(event, CallbackQuery):
                await event.answer(i18n("errors/flood"), show_alert=True)
            if isinstance(event, Message):
                return
                try:
                    await event.react(
                        reaction=[ReactionTypeEmoji(emoji=str(choice(["🗿", "👻", "🌚", "🦄"])))]
                    )
                except Exception:
                    pass
            return 

        self.limit[user_id] = True
        return await handler(event, data)
