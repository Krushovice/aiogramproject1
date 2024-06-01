from aiogram import Router, F
from aiogram.types import CallbackQuery


from api.markups import (
    MenuCbData,
    MenuActions,
    build_main_kb,
)

from utils import LEXICON


router = Router(name=__name__)
