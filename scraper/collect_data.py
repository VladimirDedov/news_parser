import requests
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scraper.nurkz import NurKz
from scraper.informburo import Informburo
from scraper.informkz import Informkz
from scraper.sko_website.pkzsk import SKO_PKZSK
from scraper.sko_website.sko_7152 import SKO_7152
from logs.config_logger import get_logger
# from parse_page import get_data_from_page_nurkz
from telegramm_bot.core.database.orm_query import write_article_to_bd

logger = get_logger(__name__)


def get_instance_of_class(url: str):
    if url == "https://www.nur.kz/":
        kz = NurKz()
    elif url == "https://pkzsk.info/":
        kz = SKO_PKZSK()
    elif url == "https://informburo.kz/novosti":
        kz = Informburo()
    elif url == "https://www.inform.kz/lenta/":
        kz = Informkz()
    elif url == "https://www.7152.kz/news":
        kz = SKO_7152()

    logger.info(f"Создан экземпляр класса {kz.__class__.__name__}")
    return kz


async def collect_data(url: str = 'https://pkzsk.info/'):
    """Парсинг данных с сайтов"""

    logger.info(f"Начинаю парсинг сайта {url}")

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

    kz = get_instance_of_class(url)

    # Получить словарь с ссылками статей и заголовками
    dict_of_article = kz.get_list_of_article(soup)
    logger.info(f"Получен словарь с ссылками статей и заголовками")
    print(dict_of_article)
    #Получить данные одной статьи - id, url, title, text для записи их в БД
    for href, article_title in dict_of_article.items():
        list_of_data = kz.get_data_from_page(href, article_title, headers)

        # Запись в базу данных
        await write_article_to_bd(list_of_data=list_of_data, is_sko=True)

        # Список айди добавленных статей
        id_article_list.append(list_of_data[1])
        list_of_data.clear()
    logger.info(f"Парсинг статей с сайта {url} окончен ")

    return id_article_list


if __name__ == "__main__":
    asyncio.run(collect_data("https://www.7152.kz/news"))
