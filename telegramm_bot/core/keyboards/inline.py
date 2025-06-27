from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegramm_bot.core.factory.call_factory import ArticleCallbackFactory, ImageCallbackFactory


def get_inline_kbd(article_id: str) -> InlineKeyboardMarkup:
    select_publish = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Опубликовать", callback_data="publish"),
                InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
            ]
        ]
    )

    return select_publish


def get_start_inline_kbd() -> InlineKeyboardMarkup:
    start_kbd = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ NUR", callback_data="nurkz"),
                InlineKeyboardButton(text="✅ ИнформБюро", callback_data="informburo"),
                InlineKeyboardButton(text="✅ ИнформКЗ", callback_data="inform"),
                InlineKeyboardButton(text="✅ Edit", callback_data="edit"),
            ],
            [
                InlineKeyboardButton(text="💥 Посмотреть статьи за сегодня", callback_data="view"),
            ]
        ]
    )

    return start_kbd


def get_view_kbd() -> InlineKeyboardMarkup:
    view_kbd = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💥 Посмотреть статьи за сегодня", callback_data="view"),
            ]
        ]
    )
    return view_kbd


def get_title_btn(
        article_id: int,
        sizes: tuple = (1,),
):
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(text="👌 Обработать в ИИ",
                                             callback_data=ArticleCallbackFactory(action="view", id=article_id).pack()
                                             ))

    return inline_keyboard.adjust(*sizes).as_markup()

def get_image_kb(index: int,
                 sizes: tuple = (1,),) -> InlineKeyboardMarkup:
    image_kbd = InlineKeyboardBuilder()

    image_kbd.add(InlineKeyboardButton(text="✏ Добавить текст",
                                             callback_data=ImageCallbackFactory(action="write", id=index).pack()
                                             ))

    return image_kbd.adjust(*sizes).as_markup()

def get_common_kbd(btns: dict,
                   sizes: tuple = (1,)):

    inline_keyboard = InlineKeyboardBuilder()
    for key, item in btns.items():
        inline_keyboard.add(InlineKeyboardButton(text=f"👌 {key}",
                                             callback_data=item
                                             ))

    return inline_keyboard.adjust(*sizes).as_markup()