from ai.gemini import get_context_from_ai
from telegramm_bot.core.database.orm_query import read_from_bd_origin_article
from telegramm_bot.core.database.orm_query import write_article_to_bd
from telegramm_bot.core.database.orm_query import write_image_to_bd
from telegramm_bot.core.database.orm_query import get_exists_neiro_article
from .image_editor import add_text_to_image
from typing import Tuple



async def create_neiro_article(id) -> Tuple[str, str, str, str, str]:
    """Обработка статьи с помощью ИИ и запись в БД"""

    # Читаем название и текст статьи с бд если существует
    tuple_of_neiro_article = await get_exists_neiro_article(id)

    if all(tuple_of_neiro_article):
        image_text, id_article, prompt_for_image, text_ai, reels_ai = tuple_of_neiro_article
    else:
        id_article, original_title, original_text = await read_from_bd_origin_article(id)  # продумать логику
        print(id_article)
        print(original_title)

        # Получаем Заголовок, содержание и текст для картинки с Нейронки
        print("Генерирую текст статьи")
        text_ai = get_context_from_ai(original_text)
        print("Генерирую заголовок статьи")
        title_ai = get_context_from_ai(original_text, title=True)
        print("Генерирую текст на картинку")
        image_text = get_context_from_ai(original_text, title=True, image_text=True)
        print("Генерирую промт для картинки")
        prompt_for_image = get_context_from_ai(text_ai, prompt=True)
        print("Генерирую текст на reels")
        reels_ai = get_context_from_ai(original_text, reels=True)
        print(f"text reels - {reels_ai}")


        # Запись в БД обработанной статьи
        list_neiro = [title_ai, text_ai, prompt_for_image, image_text, reels_ai]
        await write_article_to_bd(list_neiro, id_article, original=False)

    return image_text, id_article, prompt_for_image, text_ai, reels_ai




async def add_text(image_path: str, image_text: str, id_article: str, list_image_path: str) -> str:
    """Добавляем текст на картинку, после чего записываем данные в БД. """
    dict_data_image = {"image_path": image_path,
                       "image_text": image_text,
                       "id_article": id_article,
                       }
    for index, path in enumerate(list_image_path):
        dict_data_image[index] = path

    if image_path:
        dict_data_image["image_path_with_text"] = add_text_to_image(image_path, image_text, id_article)

    # Записываем в базу id_article, image_path, image_path_with_text, image_text
    await write_image_to_bd(dict_data_image)
    return dict_data_image["image_path_with_text"]
