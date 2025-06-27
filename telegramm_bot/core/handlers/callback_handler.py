from aiogram import types, Bot
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext

from scraper.collect_data import collect_data
from .common_handler_func import edit_article_with_ai_func, process_add_text_to_image_func, show_result_article_func, \
    publish_article_func
from ..database.orm_query import read_all_today_article
from ..keyboards.inline import get_view_kbd, get_title_btn
from ..factory.call_factory import ArticleCallbackFactory, ImageCallbackFactory

callback_router = Router()


@callback_router.callback_query(F.data == "nurkz")
async def callback_start_parse_nurkz_call(callback: types.CallbackQuery):
    await callback.message.answer(" 💭 Парсинг статей с сайта NURKZ запущен")
    await collect_data("https://www.nur.kz/")
    await callback.message.answer("Парсинг статей с сайта NURKZ окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "tengri")
async def callback_start_parse_tengri_call(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта Tengri запущен")
    await collect_data("https://tengrinews.kz/")
    await callback.message.answer("Парсинг статей с сайта Tengri окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "informburo")
async def callback_start_parse_informburo_call(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта Ифнормбюро запущен")
    await collect_data("https://informburo.kz/novosti")
    await callback.message.answer("Парсинг статей с сайта Ифнормбюро окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "inform")
async def callback_start_parse_inform_call(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта ИфнормКЗ запущен")
    await collect_data("https://www.inform.kz/lenta/")
    await callback.message.answer("Парсинг статей с сайта ИфнормКЗ окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "view")
async def get_today_articles_call(callback: types.CallbackQuery):
    await callback.message.answer("Вот список не просмотренных статей за сегодня. /edit - ввести номер статьи для "
                                  "обработки")
    dict_of_article = await read_all_today_article()
    for id, article_title in dict_of_article.items():
        await callback.message.answer(f"{id} - {article_title}", reply_markup=get_title_btn(article_id=id))


@callback_router.callback_query(ArticleCallbackFactory.filter())
async def edit_article_call(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory, state: FSMContext):
    """Выбор и запуск обработки статьи в ИИ"""
    await callback.message.answer(f"Выбрана статья - {callback_data.id}")
    await callback.message.answer(f"Выбрана статья - {type(callback.message)}")
    await edit_article_with_ai_func(callback.message, state, callback_data.id)


@callback_router.callback_query(ImageCallbackFactory.filter())
async def process_add_text_to_image_call(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory,
                                         state: FSMContext):
    await process_add_text_to_image_func(callback.message, state, callback_data.id)


@callback_router.callback_query(F.data == "show_article")
async def show_result_article_call(callback: types.CallbackQuery, state: FSMContext):
    await show_result_article_func(callback.message, state, True)


@callback_router.callback_query(F.data == "is_publish")
async def publish_article_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await publish_article_func(callback.message, state, bot, True)
    await callback.message.answer('Статья опубликована в канале')
    await state.clear()


@callback_router.callback_query(F.data == "cansel")
async def cansel_call(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Все данные очищены. Обработка статьи окончена.')
    await state.clear()
