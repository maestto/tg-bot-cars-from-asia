import asyncio
from typing import List, Dict, Union, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = 2):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return  # Don't propagate the event
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)