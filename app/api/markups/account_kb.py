from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .main_kb import MenuCbData, MenuActions


class ProfileActions(IntEnum):
    register = auto()
    card = auto()
    wish_list = auto()
    check_list = auto()
    top = auto()
    back_to_profile = auto()
    back_to_root = auto()
    read = auto()


class ProfileCbData(CallbackData, prefix="account"):
    action: ProfileActions
    book_title: str | None = None


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


def build_book_interaction_kb(book_cb_data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Читаем? ✍️",
        callback_data=ProfileCbData(
            action=ProfileActions.read,
            book_title=book_cb_data,
        ).pack(),
    )
    builder.button(
        text="Что-то другое 🔄",
        callback_data=MenuCbData(action=MenuActions.advice).pack(),
    )
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_root).pack(),
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


def register_profile(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]

        [builder.button(text=txt) for txt in text]
        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    elif isinstance(text, list):
        text = text
        [builder.button(text=txt) for txt in text]
        builder.adjust(3)
        return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
