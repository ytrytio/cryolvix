from typing import Callable, Any, Awaitable, ParamSpec, Concatenate
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

from cryolvix.database.session import get_async_session

P = ParamSpec("P")
R = Awaitable[Any]

def database(
    func: Callable[Concatenate[AsyncSession, P], R]
) -> Callable[P, R]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        session_from_kwargs = kwargs.pop("session", None)
        if isinstance(session_from_kwargs, AsyncSession):
            return await func(session_from_kwargs, *args, **kwargs)
        async with get_async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper
