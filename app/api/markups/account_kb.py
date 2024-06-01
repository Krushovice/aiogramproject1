from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ProfileActions(IntEnum):
    register = auto()
    card = auto()
    wish_list = auto()
    check_list = auto()
    top = auto()
    back_to_profile = auto()
    back_to_root = auto()


class ProfileCbData(CallbackData, prefix="account"):
    action: ProfileActions


def build_account_kb(
    is_register: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not is_register:
        builder.button(
            text="Заполнить профиль 📝",
            callback_data=ProfileCbData(action=ProfileActions.register).pack(),
        )

    else:
        builder.button(
            text="Карточка читателя 🗂",
            callback_data=ProfileCbData(action=ProfileActions.card).pack(),
        )

    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_root).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def build_book_card_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Топ 5 книг 💯",
        callback_data=ProfileCbData(action=ProfileActions.top).pack(),
    )
    builder.button(
        text="Список прочитанного 📚✅",
        callback_data=ProfileCbData(action=ProfileActions.check_list).pack(),
    )
    builder.button(
        text="Хочу прочесть 📋",
        callback_data=ProfileCbData(action=ProfileActions.wish_list).pack(),
    )
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_profile).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def root_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_root).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
