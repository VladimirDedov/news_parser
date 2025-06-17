import re
import requests

from scraper.main_article_class import Article
from bs4 import BeautifulSoup
from typing import List, Dict

class Informkz(Article):
    def __init__(self):
        self.__url: str = 'https://inform.kz'
        self.__list_of_data_from_article = []

    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        dict_of_article = {}
        article_html_list = []
        count = 0

        article_html_list = soup.find_all("div", class_="allNewsCard")


        for item in article_html_list:  # получаем список статей со сслыками на них
            tag_a = item.find("a")
            tag_div_in_a = tag_a.find("div", class_="allNewsCard_title")
            text_article=tag_div_in_a.text
            href = tag_a['href']
            dict_of_article[href] = text_article.strip()

            if count > 6:
                break
            count += 1
        return dict_of_article

    @staticmethod
    def __parse_text_from_tags_p(list_tags_p: List[str]) -> str:
        """Возвращает текст статьи из тегов p"""

        text: str = ''''''
        for p in list_tags_p:
            #text += p.find(text=True)
            if st := p.find(text=True):
                text += st

        return re.sub(r"\s+", " ", text)

    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        """Получение данных с одной статьи для записи в БД"""
        list_of_data_from_article = []
        url = self.__url+href
        id_article = href[-1:-15:-1].replace('/', '-')
        list_of_data_from_article = [id_article, url, article_title]

        responce = requests.get(url=url, headers=headers)
        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, "lxml")
        tag_div_description = soup.find("div", class_="article__description")
        text_discription = tag_div_description.find("p").find(text=True)

        tag_div = soup.find("div", class_="article__body-text")
        list_tags_p = tag_div.find_all('p')

        list_of_data_from_article.append(text_discription + Informkz.__parse_text_from_tags_p(list_tags_p))

        return list_of_data_from_article