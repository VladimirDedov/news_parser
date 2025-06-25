from aiogram.filters.callback_data import CallbackData

class ArticleCallbackFactory(CallbackData, prefix="article"):
    action: str
    id: int