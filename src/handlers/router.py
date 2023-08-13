from typing import Callable

from telebot import types

from src.handlers.analytics import analytics_general_menu_callback
from src.handlers.delete_feeding import delete_record
from src.handlers.main import add_record
from src.handlers.main import help as help_command_callback
from src.handlers.main import list_for_today
from src.handlers.main import start as start_command_callback
from src.infrastructure.telegram import bot
from src.keyboards.constants import Commands, Menu

__all__ = ("any_message",)

ROOT_COMMANDS_MAPPER: dict[str, Callable] = {
    Commands.START: start_command_callback,
    Commands.HELP: help_command_callback,
    Commands.DELETE: delete_record,
}


ROOT_MESSAGES_MAPPER: dict[str, Callable] = {
    Menu.ANALYTICS: analytics_general_menu_callback,
    Menu.TODAY: list_for_today,
}


@bot.message_handler(func=lambda message: True)
async def any_message(message: types.Message):
    assert message.text

    if _callback := ROOT_COMMANDS_MAPPER.get(message.text.split("@")[0]):
        return await _callback(message)

    if _callback := ROOT_MESSAGES_MAPPER.get(message.text):
        return await _callback(message)

    if _callback := ROOT_COMMANDS_MAPPER.get(message.text[:4]):
        return await _callback(message)

    return await add_record(message)
