from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DBMiddleware(BaseMiddleware):
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.pool = pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        async with self.pool() as async_session:
            data["db"] = async_session
            result = await handler(event, data)
            del data["db"]
        return result
