import requests
from bs4 import BeautifulSoup


def parse_text_from_tags_p(list_tags_p) -> str:
    """Возвращает текст статьи из тегов p"""

    text: str = ''''''
    for tag in list_tags_p:
        text += tag.text

    return text


def get_data_from_page_nurkz(href, title_article, headers: list, url: str) -> list:
    """Возращает список данных из статьи. id, url, title, text"""

    url = f"https://www.nur.kz" + href
    list_of_data_from_article = [href[-1:-15:-1].replace('/', '-'), url, title_article]

    responce = requests.get(url=url, headers=headers)
    responce.encoding = 'utf-8'

    soup = BeautifulSoup(responce.text, "lxml")

    list_tags_p = soup.find_all('p', class_="align-left formatted-body__paragraph")

    list_of_data_from_article.append(parse_text_from_tags_p(list_tags_p))

    return list_of_data_from_article
