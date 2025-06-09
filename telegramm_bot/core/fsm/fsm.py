"""Данные Машины состояний """

from aiogram.fsm.state import StatesGroup, State


class Add_Neiro_Article(StatesGroup):
    id = State()
    id_image = State()
    is_publish = State()
    show_result = State()

