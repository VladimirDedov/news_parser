import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from parse_page import get_data_from_page_nurkz
from bd import write_to_bd

def collect_data():
    dict_of_article: dict = {}
    href: str
    text_article: str

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

    for href, article_title in dict_of_article.items():
        list_of_data = get_data_from_page_nurkz(href, article_title, headers, url)# Получение списка данных одной статьи
        write_to_bd(list_of_data)#Запись в базу данных
        break
    # print(dict_of_article)


def main():
    collect_data()


if __name__ == "__main__":
    main()
