from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from src.keyboards.constants import Menu
from src.keyboards.models import CallbackItem


def default_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(Menu.ANALYTICS, Menu.TODAY)

    return markup


def build_callback_keyboard(patterns: list[CallbackItem], width: int = 2) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for idx, item in enumerate(patterns):
        row.append(
            InlineKeyboardButton(
                text=item.name,
                callback_data=item.callback_data,
            )
        )

        if (idx + 1) % width == 0 or idx == len(patterns) - 1:
            keyboard.append(row)
            row = []

    return InlineKeyboardMarkup(keyboard)
