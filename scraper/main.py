import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from parse_page import get_data_from_page_nurkz
from bd import write_article_to_bd, read_from_bd_origin_article
from ai.ai_generate import get_context_from_ai, get_url_image_from_ai
from scraper.bd import write_image_to_bd
from scraper.image_downloader import download_image
from Scraper_News.BingImageCreator.src.bing_main import create_bing_image
from image_editor import add_text_to_image


def collect_data():
    dict_of_article: dict = {}
    href: str
    text_article: str
    id_article_list = []
    count: int = 0

    ua = UserAgent()
    headers = {"user-agent": f"{ua.random}"}
    url = f"https://www.nur.kz/"
    responce = requests.get(url=url, headers=headers)
    responce.encoding = 'utf-8'
    soup = BeautifulSoup(responce.text, "lxml")
    article_html_list = soup.find_all("a", class_="article-card__title")

    for item in article_html_list:  # получаем список статей со сслыками на них
        text_article = item.text
        href = item['href']
        dict_of_article[href] = text_article.strip()

    for href, article_title in dict_of_article.items():
        # Получение списка данных одной статьи
        list_of_data = get_data_from_page_nurkz(href, article_title, headers, url)
        # Запись в базу данных
        write_article_to_bd(list_of_data)
        # Список айди добавленных статей
        id_article_list.append(list_of_data[1])
        list_of_data.clear()
        count += 1
        if count == 2:
            break  # Заглушка, потом убрать

    # Читаем название и текст статьи с бд
    id_article, original_title, original_text = read_from_bd_origin_article(id_article_list[1])  # продумать логику

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
    # Генерируем картинку. промпт - оригинальный заголовок
    create_bing_image(prompt_for_image, id_article)
    #Отправить все данные в телеграмм СОЗДАТЕЛЮ, с правом выбора картинки - это потом
    image_path_with_text, image_path = add_text_to_image(id_article, image_text)

    # # Записываем в базу id_article, image_url, image_path, image_text
    list_image = [id_article, image_path, image_path_with_text, image_text]
    write_image_to_bd(list_image)


def main():
    collect_data()


if __name__ == "__main__":
    main()
