from aiogram import Router, F
from aiogram.types import CallbackQuery

from api.markups import (
    ProfileActions,
    ProfileCbData,
    build_book_card_kb,
    build_account_kb,
)

from utils import LEXICON


router = Router(name=__name__)
