from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegramm_bot.core.factory.call_factory import ArticleCallbackFactory


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
        *,
        article_id: str,
        sizes: tuple = (1,),
):
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(text="👌 Обработать в ИИ",
                                             callback_data=ArticleCallbackFactory(action="view", id=article_id).pack()
                                             ))

    return inline_keyboard.adjust(*sizes).as_markup()
