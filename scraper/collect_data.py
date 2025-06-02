import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from flask import session

from .parse_page import get_data_from_page_nurkz
from Scraper_News.telegramm_bot.core.database.orm_query import write_article_to_bd


async def collect_data(session, domain: str = 'https://www.nur.kz/'):
    """Парсинг данных с сайтов"""

    dict_of_article: dict = {}
    href: str
    text_article: str
    id_article_list = []
    count = 0

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
        if count > 3:
            break
        count +=1

    for href, article_title in dict_of_article.items():
        # Получение списка данных одной статьи
        list_of_data = get_data_from_page_nurkz(href, article_title, headers, url)
        print(list_of_data)
        # Запись в базу данных
        await write_article_to_bd(list_of_data = list_of_data)
        # Список айди добавленных статей
        id_article_list.append(list_of_data[1])
        list_of_data.clear()

    return id_article_list

def main():
    collect_data()


if __name__ == "__main__":
    main()
