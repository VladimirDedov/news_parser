from aiogram import types
from aiogram import Router
from aiogram import F

from scraper.collect_data import collect_data
from ..database.orm_query import read_all_today_article
from ..keyboards.inline import get_view_kbd, get_title_btn
from ..factory.call_factory import ArticleCallbackFactory

callback_router = Router()


@callback_router.callback_query(F.data == "nurkz")
async def callback_start_parse_nurkz(callback: types.CallbackQuery):
    await callback.message.answer(" 💭 Парсинг статей с сайта NURKZ запущен")
    await collect_data("https://www.nur.kz/")
    await callback.message.answer("Парсинг статей с сайта NURKZ окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "tengri")
async def callback_start_parse_tengri(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта Tengri запущен")
    await collect_data("https://tengrinews.kz/")
    await callback.message.answer("Парсинг статей с сайта Tengri окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "informburo")
async def callback_start_parse_informburo(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта Ифнормбюро запущен")
    await collect_data("https://informburo.kz/novosti")
    await callback.message.answer("Парсинг статей с сайта Ифнормбюро окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "inform")
async def callback_start_parse_inform(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта ИфнормКЗ запущен")
    await collect_data("https://www.inform.kz/lenta/")
    await callback.message.answer("Парсинг статей с сайта ИфнормКЗ окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "view")
async def get_today_articles(callback: types.CallbackQuery):
    await callback.message.answer("Вот список не просмотренных статей за сегодня. /edit - ввести номер статьи для "
                                  "обработки")
    dict_of_article = await read_all_today_article()
    for id, article_title in dict_of_article.items():
        await callback.message.answer(f"{id} - {article_title}", reply_markup=get_title_btn(article_id=id))


@callback_router.callback_query(ArticleCallbackFactory.filter())
async def edit_article(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory):
    await callback.message.answer(f"Выбрана статья - {int(callback_data.id)}")