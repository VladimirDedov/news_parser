import os
from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from scraper.collect_data import collect_data
from ..database.orm_query import read_all_today_article
from ..fsm.fsm import Add_Neiro_Article as state_fsm
from ai.edit_article_with_ai import create_neiro_article
from ai.edit_article_with_ai import add_text
from Scraper_News.BingImageCreator.src.bing_main import create_bing_image


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
    await message.answer("Парсинг статей с сайта NURKZ окончен. Посмотреть статьи за сегодня /view")


@parse_router.message(Command("view"))
async def get_today_articles(message: types.Message):
    await message.answer("Вот список не просмотренных статей за сегодня. /edit - ввести номер статьи для обработки")
    dict_of_article = await read_all_today_article()
    for id, article_title in dict_of_article.items():
        await message.answer(f"{id} - {article_title}")


# Работа с машиной состояний. Выбор айди статьи и генерация её нейронной версии
@parse_router.message(Command("edit"))
async def get_today_articles(message: types.Message, state: FSMContext):
    await message.answer('Введите номер статьи:')
    await state.set_state(state_fsm.id)


@parse_router.message(state_fsm.id)
async def edit_article_with_ai(message: types.Message, state: FSMContext):
    id = message.text
    await message.answer(f"Выбрана статья номер - {id}!")
    await message.answer(f"Начинаю обработку статьи - {id}")

    # Обработка статьи нейросетью и создание картинок
    image_text, id_article, prompt_for_image = await create_neiro_article(id)
    await message.answer(f"Статья обработана в нейросети")
    await message.answer(f"Начинаю генерацию картинок - {id}")

    # Генерация картинки
    list_image_path = create_bing_image(prompt_for_image, id_article)
    await message.answer(f"картинки сгенерированы. ")

    # отправляем картинки на выбор для обработки
    for index, path in enumerate(list_image_path):
        photo = FSInputFile(path)
        await message.answer(f"{index}")
        await message.answer_photo(photo)

    # Запрашиваем номер картинки, для добавления текста
    await message.answer('Выберите номер картинки на какую добавить текст:')
    await state.update_data(list_image_path=list_image_path)
    await state.update_data(image_text=image_text)
    await state.update_data(id_article=id_article)
    await state.set_state(state_fsm.id_image)


@parse_router.message(state_fsm.id_image)
async def process_add_text_to_image(message: types.Message, state: FSMContext):
    id_image = int(message.text)
    data = await state.get_data()
    image_path = data.get("list_image_path")[id_image]
    image_text = data.get("image_text")
    id_article = data.get("id_article")
    list_image_path = data.get("list_image_path")
    await message.answer(f"Добавляю текст на картинку - {image_text}")
    image_path = await add_text(image_path, image_text, id_article, list_image_path)
    await message.answer(f"Текст добавлен. Вот что получилось:")
    photo = FSInputFile(image_path)
    await message.answer_photo(photo=photo)
    await state.clear()


@parse_router.message(Command("publish", "pub"))
async def process_add_text_to_image(message: types.Message, state: FSMContext):
    """Выбать пример обработанной статьи с картинкой и текстом"""
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")