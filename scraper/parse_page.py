import requests
from bs4 import BeautifulSoup
from lxml.html.defs import list_tags


def parse_text_from_tags_p(list_tags_p) -> str:
    text: str = ''''''
    for tag in list_tags_p:
        text += tag.text
    print(text)
    return text.replace('"','').replace("'",'')


def get_data_from_page_nurkz(href, name_article, headers: list, url: str) -> list:
    url = f"https://www.nur.kz"+href
    list_of_data_from_article = [href[-1:-15:-1], url, name_article]
    responce = requests.get(url=url, headers=headers)
    responce.encoding = 'utf-8'
    soup = BeautifulSoup(responce.text, "lxml")
    list_tags_p = soup.find_all('p', class_="align-left formatted-body__paragraph")
    list_of_data_from_article.append(parse_text_from_tags_p(list_tags_p))
    print(list_of_data_from_article)
    return list_of_data_from_article