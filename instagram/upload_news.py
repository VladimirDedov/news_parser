from instagrapi import Client
import sys
import os
from config import INST_PASS, INST_LOGIN

SESSION_FILE = "session.json"
USERNAME = INST_LOGIN
PASSWORD = INST_PASS


def get_client():
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        cl.login(USERNAME, PASSWORD)
    else:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
    return cl


def upload_photo(cl, path: str, caption: str = ""):
    media = cl.photo_upload(path=path, caption=caption)
    print(f"✅ Фото опубликовано: https://instagram.com/p/{media.code}/")


def upload_video(cl, path, caption=""):
    media = cl.video_upload(path=path, caption=caption)
    print(f"✅ Видео опубликовано: https://instagram.com/p/{media.code}/")


def upload_story(cl, path, caption=""):
    media = cl.photo_upload_to_story(path=path, caption=caption)
    print(f"✅ Сторис опубликована: https://instagram.com/stories/{USERNAME}/{media.pk}/")


def run_upload_instagram(caption: str = "", photo_path: str = "", is_photo: bool = True, is_video: bool = False,
                         is_story: bool = False):
    cl = get_client()
    print(photo_path, caption, sep="*****************")
    if is_photo and photo_path:
        upload_photo(cl, path=photo_path, caption=caption)
    # caption = "На Казахстанской бирже 25 сентября доллар стоил 541,68 тенге, подешевев за день на 0,92 тенге.  Средние курсы обмена валют в пунктах страны варьировались.  Ноябрьские фьючерсы на нефть Brent торговались по 69 долларов за баррель.  Динамика валютного рынка отражает текущую экономическую ситуацию.  Более подробная информация о колебаниях курса доступна на специализированных финансовых ресурсах.  Анализ показателей позволяет оценить тенденции и прогнозировать дальнейшее изменение стоимости доллара относительно тенге."
    # path = "/home/vvv/Python/news_parser/images/prepared_image/final-airbaitnes-52-.jpeg"
