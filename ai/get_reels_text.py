import time
import random
import asyncio

from telegramm_bot.core.database.orm_query import read_all_original_artical_text
from telegramm_bot.core.database.orm_query import read_image_paths
from telegramm_bot.core.database.orm_query import write_reeels_text_to_bd
from telegramm_bot.core.database.orm_query import save_list_image_path_to_bd
from ai.gemini import get_context_from_ai
from BingImageCreator.src.bing_main import create_bing_image


async def get_reels_context_from_ai():
    """генерирует текст для рилсов с помощью Гемини"""
    list_today_articles = await read_all_original_artical_text()
    print(f"Выбрано {len(list_today_articles)} статей")
    for tpl in list_today_articles:
        dct_for_write_to_bd_image_path = {}
        list_image_path = []

        id_article, text_original_article, prompt_for_image = tpl
        reels_text = get_context_from_ai(text_original_article, reels=True)  # получаем текст рилса

        if not prompt_for_image:
            print("Генерирую промт для картинки")
            prompt_for_image = get_context_from_ai(text_original_article, prompt=True)

        print(reels_text)
        # генерим картинки
        # получить пути картинок, если есть, чтобы не генерировать заново
        list_image_path = await read_image_paths(id_article)

        if list_image_path:
            print(f"Картинки была сгенерированы ранее - {id}")
        else:
            list_image_path = create_bing_image(prompt_for_image, id_article)  # Генерация картинки, если нет в БД

            if list_image_path is None:
                print(f"картинки не сгенерированы. ")
                print(f"Скорее всего запрос заблокирован Bing /edit - начать заново")

            try:
                # Сохраняем пути картинок в БД
                dct_for_write_to_bd_image_path['id_article'] = id_article
                for index, value in enumerate(list_image_path):
                    dct_for_write_to_bd_image_path[f"path_{index}"] = value
                await save_list_image_path_to_bd(dct_for_write_to_bd_image_path)
                #Сохраняем текст рилса и промпт для картинки в БД
                await write_reeels_text_to_bd(id_article, reels_text, prompt_for_image)
            except Exception as e:
                print(e)
                continue

        time.sleep(random.randint(10, 20))


if __name__ == '__main__':
    asyncio.run(get_reels_context_from_ai())
