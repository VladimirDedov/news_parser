from aiogram import types, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from config import CHAT_ID
from ..database.orm_query import read_image_path_with_text, read_image_paths
from ..database.orm_query import write_is_publised_article, save_list_image_path_to_bd
from ..fsm.fsm import Add_Neiro_Article as state_fsm
from ai.edit_article_with_ai import create_neiro_article
from ai.edit_article_with_ai import add_text
from ..keyboards.inline import get_image_kb, get_common_kbd
from BingImageCreator.src.bing_main import create_bing_image
from instagram.upload_news import run_upload_instagram

from logs.config_logger import get_logger

chat_id = CHAT_ID

logger = get_logger(__name__)
logger.info("Начинаю запуск бота")


async def edit_article_with_ai_func(message: types.Message, state: FSMContext, id: int = None):
    dct_for_write_to_bd_image_path = {}
    if not id:
        id = message.text

    await message.answer(f"Выбрана статья номер - {id}!")
    logger.info(f"Начинаю обработку статьи в нейросети с id - {id}")
    await message.answer(f"Начинаю обработку статьи - {id}")

    # Обработка статьи нейросетью
    image_text, id_article, prompt_for_image, article_neiro_text = await create_neiro_article(id)
    await state.update_data(image_text=image_text)
    await state.update_data(id_article=id_article)
    await state.update_data(article_neiro_text=article_neiro_text)
    await message.answer(f"Статья обработана в нейросети")
    logger.info(f"Статья {id} обработана в нейросети")
    await message.answer(f"Начинаю генерацию картинок - {id}")
    logger.info(f"Начата генерация картинок для статьи {id}")

    list_image_path= await read_image_paths(id_article)#получить пути картинок, если есть, чтобы не генерировать заново
    print(f"Пути картинок - {list_image_path} , id_article - {id_article}")

    if list_image_path:
        await message.answer(f"Картинки была сгенерированы ранее - {id}")
    else:
        list_image_path = create_bing_image(prompt_for_image, id_article)# Генерация картинки

        if list_image_path is None:
            await message.answer(f"картинки не сгенерированы. ")
            await message.answer(f"Скорее всего запрос заблокирован Bing /edit - начать заново")
            return False

    await message.answer(f"картинки сгенерированы. ")

    # отправляем картинки на выбор для обработки
    for index, path in enumerate(list_image_path):
        if path:
            photo = FSInputFile(path)
            await message.answer(f"{index}")
            await message.answer_photo(photo, reply_markup=get_image_kb(index))

    #Сохраняем пути картинок в БД
    dct_for_write_to_bd_image_path['id_article']=id_article
    for index, value in enumerate(list_image_path):
        dct_for_write_to_bd_image_path[f"path_{index}"] = value

    print(f"dct_for_write_to_bd_image_path - {dct_for_write_to_bd_image_path}")
    await save_list_image_path_to_bd(dct_for_write_to_bd_image_path)

    # Запрашиваем номер картинки, для добавления текста
    await state.update_data(list_image_path=list_image_path)

    await state.set_state(state_fsm.id_image)
    return True


async def process_add_text_to_image_func(message: types.Message, state: FSMContext, id_imag=None):
    """Добавление текста на картинку, если она сгенерирована Мелкомягкими"""
    if id_imag is not None:  # Проблема когда выбираешь картинку с нулевым индексом. Переработать!
        print(f"id_image {type(id_imag)} - {id_imag}")
        # id_imag = int(message.text)

    logger.info(f"Выбрана картинка для добавления текста {id_imag}")
    data = await state.get_data()
    image_path = data.get("list_image_path")[id_imag]
    image_text = data.get("image_text")
    id_article = data.get("id_article")

    list_image_path = data.get("list_image_path")
    await message.answer(f"Добавляю текст на картинку - {image_text}")

    image_path = await add_text(image_path, image_text, id_article, list_image_path)
    await message.answer(f"Текст добавлен.", reply_markup=get_common_kbd({"Показать статью": "show_article",
                                                                          "Cansel": "cansel"},
                                                                         sizes=(2,)))
    logger.info(f"Текст на картинку {id_imag} добавлен")
    await state.update_data(image_path=image_path)
    await state.update_data(id_article=id_article)
    await state.set_state((state_fsm.show_result))


async def show_result_article_func(message: types.Message, state: FSMContext, show_result: bool = False):
    """Показать рещультат в телеграмм боте"""
    if not show_result:
        show_result = int(message.text)

    if show_result:
        data = await state.get_data()
        article_neiro_text = data.get("article_neiro_text")
        image_path = data.get("image_path")
        photo = FSInputFile(image_path)
        await message.answer_photo(photo=photo, caption=article_neiro_text, parse_mode=ParseMode.HTML,
                                   reply_markup=get_common_kbd({"Опубликовать в канале?": "is_publish",
                                                                "Опубликовать в Инсте?": "is_publish_inst",
                                                                "Cansel": "cansel"},
                                                               sizes=(2,)))
        await state.update_data(photo=photo)
        await state.update_data(caption=article_neiro_text)
        logger.info(f"Показана готовая статья в телеграмм боте")
        await state.set_state(state_fsm.is_publish)
    else:
        await message.answer('Все данные очищены. Обработка статьи окончена.')
        await state.clear()


async def publish_article_func(message: types.Message, state: FSMContext, bot: Bot, is_publish: bool = False):
    """Публикация статьи в Телграмм канал"""
    if not is_publish:
        is_published = message.text

    if is_publish:
        data = await state.get_data()
        photo = data.get("photo")
        caption = data.get("caption")
        id_article = data.get("id_article")
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        await write_is_publised_article(id_article)
        logger.info(f"Статья опубликована в канале")


async def publish_article_inst_func(message: types.Message, state: FSMContext, bot: Bot, is_publish: bool = False):
    """Публикация статьи в Телграмм канал"""
    if not is_publish:
        is_published = message.text

    if is_publish:
        data = await state.get_data()
        image_path = data.get("image_path")
        caption = data.get("caption")
        id_article = data.get("id_article")
        run_upload_instagram(photo_path=image_path, caption=caption, is_photo=True)
        logger.info(f"Статья опубликована в Инстаграмме")
