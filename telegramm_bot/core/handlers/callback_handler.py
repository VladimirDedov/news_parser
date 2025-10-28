from aiogram import types, Bot
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext

from scraper.collect_data import collect_data
from .common_handler_func import edit_article_with_ai_func
from .common_handler_func import show_result_article_func
from .common_handler_func import publish_article_inst_func
from .common_handler_func import process_add_text_to_image_func
from .common_handler_func import publish_article_func

from ..database.orm_query import read_all_today_article, mark_artical_for_prepared_for_reels
from ..keyboards.inline import get_view_kbd, get_title_btn, get_start_inline_kbd
from ..keyboards.inline import get_add_text_to_image_kbd
from ..factory.call_factory import ArticleCallbackFactory, ImageCallbackFactory
from ai.get_reels_text import get_reels_context_from_ai
from ai.image_editor import add_text_to_reels_image

callback_router = Router()


@callback_router.callback_query(F.data == "nurkz")
async def callback_start_parse_nurkz_call(callback: types.CallbackQuery):
    """"""
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


@callback_router.callback_query(F.data == "pkzsk")
async def callback_start_parse_pkzsk_call(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта PKZSK запущен")
    await collect_data("https://pkzsk.info/")
    await callback.message.answer("Парсинг статей с сайта PKZSK окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "sko_7152")
async def callback_start_parse_7152_call(callback: types.CallbackQuery):
    await callback.message.answer("💭 Парсинг статей с сайта 7152 запущен")
    await collect_data("https://www.7152.kz/news")
    await callback.message.answer("Парсинг статей с сайта 7152 окончен. Посмотреть статьи за сегодня /view",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "add_text_to_image_kbd")
async def add_text_to_image_kbd(callback: types.CallbackQuery):
    """Добавление текста на картинку для Reels"""
    await callback.message.answer("💭 Добавляю текст на картинки Рилс")
    await add_text_to_reels_image()
    await callback.message.answer("Текст на картинки добавлен",
                                  reply_markup=get_view_kbd())


@callback_router.callback_query(F.data == "view")
async def get_today_articles_call(callback: types.CallbackQuery):
    """Выбираем список статей за сегодня, возле id в скобках помечена ли статья для рилс"""
    await callback.message.answer("Вот список не просмотренных статей за сегодня. /edit - ввести номер статьи для "
                                  "обработки")
    lst_of_article = await read_all_today_article()
    for tpl in lst_of_article:
        id, article_title, is_reels = tpl
        await callback.message.answer(f"{id} ({is_reels})- {article_title}", reply_markup=get_title_btn(article_id=id))


@callback_router.callback_query(F.data == "get_reels_text_from_ai")
async def get_text_for_reels(callback: types.CallbackQuery):
    #  обработка статей в нейросети для генерации рилса и картинок
    await callback.message.answer("Начинаю обработку статей для рилс!")
    await get_reels_context_from_ai()
    await callback.message.answer("Статьи обработаны!", reply_markup=get_add_text_to_image_kbd())


@callback_router.callback_query(ArticleCallbackFactory.filter(F.action == "reels"))
async def mark_for_reels(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory):
    #  помечаем статью для рилс, поле prepared_for_reels ставим в 1
    article_id = callback_data.id
    try:
        await mark_artical_for_prepared_for_reels(article_id)
        await callback.answer("✅ Статья помечена для рилс!", show_alert=False)
    except Exception as e:
        print(f"Статья с id - {article_id} не помечена, ошбка - {e}")


@callback_router.callback_query(ArticleCallbackFactory.filter())
async def edit_article_call(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory, state: FSMContext):
    """Выбор и запуск обработки статьи в ИИ"""
    # await callback.message.answer(f"Выбрана статья - {callback_data.id}")
    flag = await edit_article_with_ai_func(callback.message, state, callback_data.id)
    if not flag:
        await callback.message.answer(f"Картинки не были сгенерированы.", reply_markup=get_start_inline_kbd())


@callback_router.callback_query(ImageCallbackFactory.filter())
async def process_add_text_to_image_call(callback: types.CallbackQuery, callback_data: ArticleCallbackFactory,
                                         state: FSMContext):
    """Добавление текста на картнку для статьи"""
    await process_add_text_to_image_func(callback.message, state, callback_data.id)


@callback_router.callback_query(F.data == "show_article")
async def show_result_article_call(callback: types.CallbackQuery, state: FSMContext):
    """Показать статью в боте"""
    await show_result_article_func(callback.message, state, True)


@callback_router.callback_query(F.data == "is_publish")
async def publish_article_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Публикация статьи в телеграмм канале"""
    await publish_article_func(callback.message, state, bot, True)
    await callback.message.answer('Статья опубликована в канале')
    await callback.message.answer("Создатель, приветствую тебя!", reply_markup=get_start_inline_kbd())
    await state.clear()


@callback_router.callback_query(F.data == "is_publish_inst")
async def publish_article_inst_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Публикация в канале и инсте, если выбрано опудбликовать в Инстре"""
    await publish_article_func(callback.message, state, bot, True)  # Опубликовать в канале телеги
    await callback.message.answer('Статья опубликована в канале Телеграмма')
    await publish_article_inst_func(callback.message, state, bot, True)  # Опубликовать в Инсте
    await callback.message.answer('Статья опубликована в Инстаграмм')
    await callback.message.answer("Создатель, приветствую тебя!", reply_markup=get_start_inline_kbd())
    await state.clear()


@callback_router.callback_query(F.data == "cansel")
async def cansel_call(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Все данные очищены. Обработка статьи окончена.')
    await callback.message.answer("Создатель, приветствую тебя!", reply_markup=get_start_inline_kbd())
    await state.clear()
