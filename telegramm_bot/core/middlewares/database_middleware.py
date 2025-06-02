from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject#TelegramObject В любой хендлер может пробрасываться событие. Не только в Message
from sqlalchemy.ext.asyncio import async_sessionmaker


#Middleware
class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool=session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session#В каждом хендлере будет доступен параметр session
            return await handler(event, data)#Обязательно так возвращать