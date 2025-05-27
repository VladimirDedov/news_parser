import requests
import os


def download_image(image_url: str, id_article: str) -> str:
    """Загрузка изображения и возврат пути, где хранится картинка"""

    response = requests.get(image_url)
    image_name = id_article + ".jpg"
    path = '/home/vvv/Python/scraper_news/Scraper_News/images/'
    image_path = os.path.join(path, image_name)

    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print("Картинка сохранена как", image_path)
    else:
        print("Ошибка при загрузке:", response.status_code)

    return image_path
