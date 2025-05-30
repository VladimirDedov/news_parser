import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.filters import CommandStart

from telegramm_bot.core.handlers.parse_handler import parse_router

load_dotenv(dotenv_path="/home/vvv/Python/scraper_news/Scraper_News/.env")
BOT_TOKEN = getenv("TOKEN_BOT")

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
dp.include_router(parse_router)


async def run_telegram_bot():
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускает обновления пока в оффлайне
    await dp.start_polling(bot)


def run_telegramm():
    asyncio.run(run_telegram_bot())
