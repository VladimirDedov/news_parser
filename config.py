import os
from dotenv import load_dotenv

load_dotenv()

COOKIE = os.getenv("BING_COOKIE")#путь до куки с сайта Bing
SRCHHPGUSR = os.getenv("BING_SRCHHPGUSR")#путь до куки SRCHHPGUSR с сайта Bing
PATH_BD = os.getenv("DB_SQLITE")#Путь до бд
BOT_TOKEN = os.getenv("TOKEN_BOT")#токен бота телеграмма
PATH_IMAGES = os.getenv("PATH_IMAGES")#Путь до папки, куда сохраняются варианты картинок
PATH_FONT = os.getenv("PATH_FONT")#Путь до шрифта надписи на картинку
PATH_FINAL_IMAGE=os.getenv("PATH_FINAL_IMAGE")#Путь до сделанной картинки, готовой к публикации