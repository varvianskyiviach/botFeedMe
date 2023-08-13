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
    keyboard = [
        [
            InlineKeyboardButton(
                text=item.name,
                callback_data=item.callback_data,
            )
            for item in patterns
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
