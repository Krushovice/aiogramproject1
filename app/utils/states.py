from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    username = State()
    books = State()
    genre = State()
    survey = State()

