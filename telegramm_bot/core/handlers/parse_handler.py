from aiogram import Router
from aiogram import types
from aiogram import Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from scraper.collect_data import collect_data
from ..database.orm_query import read_all_today_article
from ..database.orm_query import read_image_path_with_text
from ..database.orm_query import write_is_publised_article
from ..fsm.fsm import Add_Neiro_Article as state_fsm
from ai.edit_article_with_ai import create_neiro_article
from ai.edit_article_with_ai import add_text
from Scraper_News.BingImageCreator.src.bing_main import create_bing_image
from config import CHAT_ID
from logs.config_logger import get_logger

logger = get_logger(__name__)
logger.info("Начинаю запуск бота")
parse_router = Router()
chat_id = CHAT_ID


@parse_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):
    await message.answer("Создатель, приветствую тебя!")


@parse_router.message(Command("nurkz"))
async def start_parse_nurkz(message: types.Message):
    await message.answer("Парсинг статей с сайта NURKZ запущен")
    id_article_list = await collect_data("https://www.nur.kz/")
    await message.answer("Парсинг статей с сайта NURKZ окончен. Посмотреть статьи за сегодня /view")


@parse_router.message(Command("tengri"))
async def start_parse_nurkz(message: types.Message):
    await message.answer("Парсинг статей с сайта Tengri запущен")
    id_article_list = await collect_data("https://tengrinews.kz/")
    await message.answer("Парсинг статей с сайта Tengri окончен. Посмотреть статьи за сегодня /view")


@parse_router.message(Command("informburo"))
async def start_parse_nurkz(message: types.Message):
    await message.answer("Парсинг статей с сайта Ифнормбюро запущен")
    id_article_list = await collect_data("https://informburo.kz/novosti")
    await message.answer("Парсинг статей с сайта Ифнормбюро окончен. Посмотреть статьи за сегодня /view")


@parse_router.message(Command("inform"))
async def start_parse_nurkz(message: types.Message):
    await message.answer("Парсинг статей с сайта ИфнормКЗ запущен")
    id_article_list = await collect_data("https://www.inform.kz/lenta/")
    await message.answer("Парсинг статей с сайта ИфнормКЗ окончен. Посмотреть статьи за сегодня /view")


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

    # Обработка статьи нейросетью
    image_text, id_article, prompt_for_image, article_neiro_text = await create_neiro_article(id)
    await state.update_data(image_text=image_text)
    await state.update_data(id_article=id_article)
    await state.update_data(article_neiro_text=article_neiro_text)
    await message.answer(f"Статья обработана в нейросети")
    await message.answer(f"Начинаю генерацию картинок - {id}")

    # Проверить существует ли картинка с текстом
    image_path_with_text = await read_image_path_with_text(id_article)
    print(f"image_path_with_text - {image_path_with_text}")
    if image_path_with_text:
        await message.answer(f"Картинка была сгенерирована ранее - {id}")
        await message.answer(f"Показать результат, готовый для публикации? 1 - Да, 0 - Нет")
        await state.update_data(image_path=image_path_with_text[0])
        await state.set_state(state_fsm.show_result)
    else:
        # Генерация картинки
        list_image_path = create_bing_image(prompt_for_image, id_article)
        if list_image_path is None:
            await message.answer(f"картинки не сгенерированы. ")
            await message.answer(f"Скорее всего запрос заблокирован Bing /edit - начать заново")
            return
        await message.answer(f"картинки сгенерированы. ")

        # отправляем картинки на выбор для обработки
        for index, path in enumerate(list_image_path):
            photo = FSInputFile(path)
            await message.answer(f"{index}")
            await message.answer_photo(photo)

        # Запрашиваем номер картинки, для добавления текста
        await message.answer('Выберите номер картинки на какую добавить текст:')
        await state.update_data(list_image_path=list_image_path)

        await state.set_state(state_fsm.id_image)


@parse_router.message(state_fsm.id_image)
async def process_add_text_to_image(message: types.Message, state: FSMContext, bot: Bot):
    id_image = int(message.text)
    data = await state.get_data()
    image_path = data.get("list_image_path")[id_image]
    image_text = data.get("image_text")
    id_article = data.get("id_article")

    list_image_path = data.get("list_image_path")
    await message.answer(f"Добавляю текст на картинку - {image_text}")
    image_path = await add_text(image_path, image_text, id_article, list_image_path)
    await message.answer(f"Текст добавлен.")
    await message.answer(f"Показать результат, готовый для публикации? 1 - Да, 0 - Нет")
    await state.update_data(image_path=image_path)
    await state.update_data(id_article=id_article)
    await state.set_state((state_fsm.show_result))


@parse_router.message(state_fsm.show_result)
async def show_result_article(message: types.Message, state: FSMContext):
    show_result = int(message.text)
    if show_result:
        data = await state.get_data()
        article_neiro_text = data.get("article_neiro_text")
        image_path = data.get("image_path")
        photo = FSInputFile(image_path)
        await message.answer_photo(photo=photo, caption=article_neiro_text)
        await state.update_data(photo=photo)
        await state.update_data(caption=article_neiro_text)
        await message.answer('Опубликовать статью? 1 - Да, 0 - Нет')
        await state.set_state(state_fsm.is_publish)
    else:
        await message.answer('Все данные очищены. Обработка статьи окончена.')
        await state.clear()


@parse_router.message(state_fsm.is_publish)
async def publish_article(message: types.Message, state: FSMContext, bot: Bot):
    """Публикация статьи в Телграмм канал"""
    is_published = int(message.text)
    if is_published:
        data = await state.get_data()
        photo = data.get("photo")
        caption = data.get("caption")
        id_article = data.get("id_article")
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        await write_is_publised_article(id_article)
    await state.clear()
