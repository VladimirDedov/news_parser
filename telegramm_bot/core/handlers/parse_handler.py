from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from scraper.collect_data import collect_data
from ..database.orm_query import read_all_today_article
from ..fsm.fsm import Add_Neiro_Article as state_fsm
from ai.edit_article_with_ai import create_neiro_article


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
    count = 0
    await message.answer("Парсинг статей с сайта NURKZ запущен")
    id_article_list = await collect_data("https://www.nur.kz/")
    await message.answer("Парсинг статей с сайта NURKZ окончен")

@parse_router.message(Command("view"))
async def get_today_articles(message: types.Message):
    await message.answer("Вот список не просмотренных статей за сегодня")
    dict_of_article = await read_all_today_article()
    for id, article_title in dict_of_article.items():
        await message.answer(f"{id} - {article_title}")

#Работа с машиной состояний. Выбор айди статьи и генерация её нейронной версии
@parse_router.message(Command("edit"))
async def get_today_articles(message: types.Message, state: FSMContext):
    await message.answer('Введите номер статьи:')
    await state.set_state(state_fsm.id)

@parse_router.message(state_fsm.id)
async def process_id(message: types.Message, state: FSMContext):
    id = message.text
    await message.answer(f"Выбрана статья номер - {id}!")
    await state.clear()
    #Обработка статьи нейросетью и создание картинок
    list_of_data = await create_neiro_article(id)
    #Генерация картинки
