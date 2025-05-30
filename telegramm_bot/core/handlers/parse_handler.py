from aiogram import Bot, Router
from aiogram import types
from aiogram.filters import CommandStart, Command

from scraper.collect_data import collect_data

parse_router = Router()

@parse_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Создатель, приветствую тебя!")
    # Запускаем парсинг collect_data()
    # Выводим список свежих статей с айдишниками считывать с базы - создать функцию читалку с базы свежих статей
    # Обрабатываем выбранную статью по id_article  create_neiro_article
    # читаем статью из базы и отправляем в телеграмм на одобрение

@parse_router.message(Command("nurkz"))
async def start_parse_nurkz(message: types.Message):
    id_article_list = collect_data("https://www.nur.kz/")
    await message.answer("Отправить список заголовков статей с номерами, для выбора, чтобы обрабатывать в ИИ")