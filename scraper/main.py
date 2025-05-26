import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml.html.builder import TITLE

from parse_page import get_data_from_page_nurkz
from bd import write_to_bd, read_from_bd_origin_article
from openai.ai import get_context_from_ai

def collect_data():
    dict_of_article: dict = {}
    href: str
    text_article: str
    id_article_list = []

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
        id_article_list.append(list_of_data[0])
        list_of_data.clear()
        break
    # print(dict_of_article)

    #Читаем название и текст статьи с бд
    original_title, original_text = read_from_bd_origin_article(id_article_list[0])
    #Полчаем Заголовок, содержание и текст для картинки с Нейронки
    text_ai = get_context_from_ai(original_text)
    title_ai = get_context_from_ai(original_text, title=True)
    text_for_image = get_context_from_ai(title_ai, title=True, image_text=True)

    print(f"title ai - {title_ai}")
    print(f"text for image - {text_for_image}")
    print(f"text - {text_ai}")

def main():
    collect_data()


if __name__ == "__main__":
    main()
