import os
from aiohttp.hdrs import COOKIE
from BingImageCreator import ImageGen
from dotenv import load_dotenv

# Загрузка данных для авторизации на сайте
load_dotenv(dotenv_path="/home/vvv/Python/scraper_news/Scraper_News/.env")
cookie = os.getenv("BING_COOKIE")
srchhp = os.getenv("BING_SRCHHP")


def create_bing_image(prompt: str, id_article: str = None) -> None:
    """Генерировать 4 картинки нейронкой Bing c айдишником статьи"""

    # Создаем экземпляр
    ig = ImageGen(auth_cookie=cookie, auth_cookie_SRCHHPGUSR=srchhp)

    try:
        # Получение ссылок на изображения
        images = ig.get_images(prompt)
        print(images)
        # Сохраняем изображения в папку
        ig.save_images(images, output_dir="/home/vvv/Python/scraper_news/Scraper_News/images/bing_image", file_name=id_article)
    except Exception as e:
        print(f"Какая то ошибка при генерации или сохранении картинок \n {e}")


