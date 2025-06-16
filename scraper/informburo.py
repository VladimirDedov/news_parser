import requests

from scraper.main_article_class import Article
from bs4 import BeautifulSoup
from typing import List, Dict


class Informburo(Article):
    def __init__(self):
        self.url: str = 'https://informburo.kz/novosti'
        self.__list_of_data_from_article = []

    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        dict_of_article = {}
        article_html_list = []
        count = 0

        article_html_list = soup.find_all("li", class_="uk-grid uk-grid-small uk-margin-remove-top")

        for item in article_html_list:  # получаем список статей со сслыками на них
            tag_div = item.find("div", class_="uk-width-expand")
            tag_a = tag_div.find("a")
            text_article = tag_a.find(text=True).strip()
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
            # st = p.find(text=True)
            if st := p.find(text=True):
                text += st

        return text

    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        """Получение данных с одной статьи для записи в БД"""
        list_of_data_from_article = []
        url = href
        id_article = href[-1:-15:-1].replace('/', '-')
        list_of_data_from_article = [id_article, url, article_title]

        responce = requests.get(url=url, headers=headers)
        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, "lxml")
        tag_div = soup.find("div", class_="uk-width-2-3@m uk-width-1-1")

        list_tags_p = tag_div.find_all('p')

        list_of_data_from_article.append(Informburo.__parse_text_from_tags_p(list_tags_p))

        return list_of_data_from_article
