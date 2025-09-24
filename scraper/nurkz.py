import requests

from scraper.main_article_class import Article
from bs4 import BeautifulSoup
from typing import List, Dict
from logs.config_logger import get_logger

logger = get_logger(__name__)


class NurKz(Article):
    def __init__(self):
        self.url: str = 'https://www.nur.kz'
        self.__list_of_data_from_article = []

    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        dict_of_article = {}
        article_html_list = []
        count = 0

        article_html_list = soup.find_all("a", class_="article-card__title")

        for item in article_html_list:  # получаем список статей со сслыками на них
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

        text: str = ''
        for tag in list_tags_p:
            text += tag.text

        return text

    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        """Получение данных с одной статьи для записи в БД"""

        logger.info(f"Начинаю обработку статьи{article_title}")

        list_of_data_from_article = []
        url = self.url + href
        id_article = href[-1:-15:-1].replace('/', '-')
        list_of_data_from_article = [id_article, url, article_title]

        responce = requests.get(url=url, headers=headers)
        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, "lxml")

        list_tags_p = soup.find_all('p', class_="align-left formatted-body__paragraph")

        list_of_data_from_article.append(NurKz.__parse_text_from_tags_p(list_tags_p))
        logger.info(f"Статья - {article_title} обработана")
        return list_of_data_from_article
