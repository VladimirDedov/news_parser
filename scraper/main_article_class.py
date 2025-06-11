from abc import abstractmethod
from typing import List, Dict
from bs4 import BeautifulSoup


class Article():
    # def __init__(self, soup=None):
    #     self.soup = soup

    @abstractmethod
    def get_list_of_article(self, soup: BeautifulSoup) -> Dict[str, str]:
        print(f"Abstract method get_list_of_data not implemented in {self.__class__}")

    @abstractmethod
    def get_data_from_page(self, href: str, article_title: str, headers: Dict[str, str]) -> List[str]:
        print(f"Abstract method get_data_from_page_nurkz not implemented in {self.__class__}")
