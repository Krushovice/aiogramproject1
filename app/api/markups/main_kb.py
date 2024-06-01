from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuActions(IntEnum):
    profile = auto()
    advice = auto()
    support = auto()
    friends = auto()
    back_root = auto()


class MenuCbData(CallbackData, prefix="main"):
    action: MenuActions


def build_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Аккаунт 👤",
        callback_data=MenuCbData(action=MenuActions.profile).pack(),
    )

    builder.button(
        text="Помощь ⚒",
        callback_data=MenuCbData(action=MenuActions.support).pack(),
    )

    builder.button(
        text="Что почитать?🧠",
        callback_data=MenuCbData(action=MenuActions.advice).pack(),
    )

    builder.button(
        text="Мои друзья ✌",
        callback_data=MenuCbData(action=MenuActions.friends).pack(),
    )
    builder.adjust(2)

    return builder.as_markup()
