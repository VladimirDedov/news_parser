from aiogram.filters.callback_data import CallbackData

class ArticleCallbackFactory(CallbackData, prefix="article"):
    action: str
    id: int

class ImageCallbackFactory(CallbackData, prefix="image"):
    action: str
    id: int