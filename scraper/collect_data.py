import requests
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from .nurkz import NurKz
from .tengri import Tengri
from .informburo import Informburo

# from parse_page import get_data_from_page_nurkz
from Scraper_News.telegramm_bot.core.database.orm_query import write_article_to_bd


async def collect_data(url: str = 'https://www.nur.kz/'):
    """Парсинг данных с сайтов"""

    dict_of_article: dict = {}
    href: str
    text_article: str
    id_article_list = []
    count = 0

    ua = UserAgent()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',  # или другой реалистичный реферер
    }
    responce = requests.get(url=url, headers=headers)
    responce.encoding = 'utf-8'
    soup = BeautifulSoup(responce.text, "lxml")

    if url == "https://www.nur.kz/":
        kz = NurKz()
    elif url == "https://www.nur.kz/":
        kz = Tengri()
    elif url == "https://informburo.kz/novosti":
        kz = Informburo()

    # Получить словарь с ссылками статей и заголовками
    dict_of_article = kz.get_list_of_article(soup)
    print(f"dict_of_article - {dict_of_article}")

    # Получить данные одной статьи - id, url, title, text для записи их в БД
    for href, article_title in dict_of_article.items():
        list_of_data = kz.get_data_from_page(href, article_title, headers)

        # Запись в базу данных
        await write_article_to_bd(list_of_data=list_of_data)
        print(f"list_of_data - {list_of_data}")
        # Список айди добавленных статей
        id_article_list.append(list_of_data[1])
        list_of_data.clear()

    return id_article_list


def main():
    asyncio.run(collect_data("https://informburo.kz/novosti"))


if __name__ == "__main__":
    main()
