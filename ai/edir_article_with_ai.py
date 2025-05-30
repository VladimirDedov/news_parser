from ai.ai_generate import get_context_from_ai
from database.bd import write_image_to_bd
from Scraper_News.BingImageCreator.src.bing_main import create_bing_image
from database.bd import read_from_bd_origin_article
from database.bd import write_article_to_bd
from image_editor import add_text_to_image

def create_neiro_article(id_article):
    """Обработка статьи с помощь ИИ и запись в БД"""
    # Читаем название и текст статьи с бд
    original_title, original_text = read_from_bd_origin_article(id_article)  # продумать логику

    # Полчаем Заголовок, содержание и текст для картинки с Нейронки
    text_ai = get_context_from_ai(original_text)
    title_ai = get_context_from_ai(original_text, title=True)
    image_text = get_context_from_ai(original_text, title=True, image_text=True)
    prompt_for_image = get_context_from_ai(text_ai, prompt=True)

    # Запись в БД обработанной статьи
    list_neiro = [title_ai, text_ai, prompt_for_image]
    write_article_to_bd(list_neiro, id_article, original=False)

    print(f"title ai - {title_ai}")
    print(f"text for image - {image_text}")
    print(f"text - {text_ai}")
    print(f"promt - {prompt_for_image}")

    # Генерируем картинку. промпт - сгенерирован нейронкой
    create_bing_image(prompt_for_image, id_article)

    # Отправить все данные в телеграмм СОЗДАТЕЛЮ, с правом выбора картинки - это потом
    image_path_with_text, image_path = add_text_to_image(id_article, image_text)

    # # Записываем в базу id_article, image_url, image_path, image_text
    list_image = [id_article, image_path, image_path_with_text, image_text]
    write_image_to_bd(list_image)
