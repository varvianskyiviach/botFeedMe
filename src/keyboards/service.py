from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.models import CallbackItem


def build_callback_keyboard(
    patterns: list[CallbackItem], width: int = 2
) -> InlineKeyboardMarkup:
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
