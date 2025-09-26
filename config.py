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
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")#Путь до ключа Gemini
CHAT_ID=os.getenv("CHAT_ID")#Имя телеграмм канала
PATH_LOG = os.getenv("PATH_LOG")
INST_LOGIN = os.getenv("INST_LOGIN")#Логин инсты Kazahstan_news
TEST_LOGIN = os.getenv("TEST_LOGIN")#Тестовый логин от vl_tik_tok
INST_PASS = os.getenv("INST_PASS")