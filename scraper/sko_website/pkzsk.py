import requests

from scraper.main_article_class import Article
from bs4 import BeautifulSoup
from typing import List, Dict
from logs.config_logger import get_logger

logger = get_logger(__name__)


class SKO_PKZSK(Article):
    def __init__(self):
        self.url: str = 'https://pkzsk.info/category/news/petronews/'
        self.__list_of_data_from_article = []

    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Возвращает словарь с ключами - сслыка на статью, данные - заголовок статьи"""
        dict_of_article = {}
        article_html_list = []
        count = 0

        article_html_list = soup.find_all("a", class_="populartitle")

        for item in article_html_list:  # получаем список статей со сслыками на них
            text_article = item.text
            href = item['href']
            dict_of_article[href] = text_article.strip()

            if count > 6:
                break
            count += 1
        return dict_of_article

    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        """Получение данных с одной статьи для записи в БД"""

        logger.info(f"Начинаю обработку статьи{article_title}")

        list_of_data_from_article = []
        url = href
        id_article = href[-1:-15:-1].replace('/', '-')
        list_of_data_from_article = [id_article, url, article_title]

        responce = requests.get(url=url, headers=headers)
        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, "lxml")

        list_tags_div = soup.find_all('div', class_="entry-content")
        # Получаем весь текст в диве с классом class_="entry-content"
        text_list = [div.get_text(separator=" ", strip=True) for div in list_tags_div]

        list_of_data_from_article.append(text_list[0])
        logger.info(f"Статья - {article_title} обработана")

        return list_of_data_from_article


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',  # или другой реалистичный реферер
    }

    responce = requests.get(
        url='https://pkzsk.info/v-rajjone-magzhana-zhumabaeva-proshel-final-selskojj-volejjbolnojj-ligi/',
        headers=headers)
    responce.encoding = 'utf-8'

    soup = BeautifulSoup(responce.text, "lxml")
    list_tags_div = soup.find_all('div', class_="entry-content")

    for div in list_tags_div:
        text_list = [div.get_text(separator=" ", strip=True) for div in list_tags_div]
    print(f"list_tags_p - {text_list}")
    print(f"text-list - {text_list[0]}")
    # list_of_data_from_article=[]
    # list_of_data_from_article.append(SKO_PKZSK.parse_text_from_tags_p(list_tags_p))
    # print(f"list_of_data_from_article - {list_of_data_from_article}")
