import asyncio
from aiogram import Bot, Dispatcher

from .core.database.engine import create_db
from .core.database.engine import session_maker
from .core.middlewares.database_middleware import DataBaseSession
from logs.config_logger import get_logger
logger = get_logger(__name__)

from telegramm_bot.core.handlers.parse_handler import parse_router

from config import BOT_TOKEN




bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
dp.include_router(parse_router)


async def run_telegram_bot():
    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))  # сессия для работы с бд
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускает обновления пока в оффлайне
    logger.info("Бот запущен")
    await dp.start_polling(bot)


def run_telegramm():
    asyncio.run(run_telegram_bot())
