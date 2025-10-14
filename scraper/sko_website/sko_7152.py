import requests
import json
import re

from click import style

from scraper.main_article_class import Article
from bs4 import BeautifulSoup
from typing import List, Dict


class SKO_7152(Article):
    def __init__(self):
        # self.url: str = 'https://www.7152.kz/news/cat/2,3,4,5,6,7,11,21,24,25,26,27,34,35,36'
        self.url: str = 'https://www.7152.kz/news'
        self.__list_of_data_from_article = []

    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        dict_of_article = {}
        article_html_list = []
        count = 0

        list_tags_a = soup.find_all('a', class_="c-news-block__title")
        list_tags_a.extend(soup.find_all('a', class_="c-news-card__title"))

        for item in list_tags_a:  # получаем список статей со сслыками на них
            text_article = item.text
            href = item['href']
            dict_of_article[href] = text_article.strip()

            if count > 6:
                break
            count += 1

        return dict_of_article

    @staticmethod
    def __parse_text_from_tags_p(list_tags_p: List[str]) -> str:
        """Возвращает текст статьи из тегов p"""

        text: str = ''''''
        for tag in list_tags_p:
            text += tag.text

        return text

    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        """Получение данных с одной статьи для записи в БД"""

        list_of_data_from_article = []
        url = href
        id_article = href[-1:-15:-1].replace('/', '-')
        list_of_data_from_article = [id_article, url, article_title]
        print("***************************")
        print(href)
        print(article_title)
        print(id_article)
        print("***************************")
        responce = requests.get(url=url, headers=headers)
        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, "lxml")

        list_tags_p = soup.find_all('p')
        print(f"p - {list_tags_p}")
        for p in list_tags_p:
            text_list = [p.get_text(separator=" ", strip=True) for p in list_tags_p]

        print(f"list_text - {text_list}")
        text = " ".join(text_list)
        print(text)
        list_of_data_from_article.append(text)

        return  list_of_data_from_article


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',  # или другой реалистичный реферер
    }

    responce = requests.get(
        url='https://www.7152.kz/news/4013611/zapertaa-na-vysote-spasateli-snali-zensinu-s-balkona-patogo-etaza-v-petropavlovske',
        headers=headers)
    responce.encoding = 'utf-8'

    soup = BeautifulSoup(responce.text, "lxml")

    #
    list_tags_p = soup.find_all('p')
    print(list_tags_p)
    #
    for p in list_tags_p:
        text_list = [p.get_text(separator=" ", strip=True) for p in list_tags_p]
    # print(f"list_tags_p - {text_list}")
    print(f"text-list - {" ".join(text_list)}")
    # list_of_data_from_article=[]
    # list_of_data_from_article.append(SKO_PKZSK.parse_text_from_tags_p(list_tags_p))
    # print(f"list_of_data_from_article - {list_of_data_from_article}")
