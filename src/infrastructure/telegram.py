import os
from contextlib import suppress
from importlib import import_module

from loguru import logger
from telebot.async_telebot import AsyncTeleBot, types

from src.setting import SRC_FOLDER, TELEGRAM_BOT_API_KEY

COMMANDS_LIST = [
    types.BotCommand("/start", "➾ start up the bot;"),
    types.BotCommand("/help", "➾ get help about commands;"),
    types.BotCommand("/today", "➾ get the list of records for today;"),
]


def create_bot(token):
    if not token:
        raise Exception("Telegram API key is not specified in the .env  ❌")

    return AsyncTeleBot(token)


def import_handlers():
    handlers_dir = SRC_FOLDER / "handlers"

    logger.debug("Loading handlers...")
    for app_name in os.listdir(handlers_dir):
        with suppress(ModuleNotFoundError, AttributeError):
            logger.success(f"{app_name} is loaded")
            import_module(f"src.handlers.{app_name}")


bot: AsyncTeleBot = create_bot(token=TELEGRAM_BOT_API_KEY)
import_handlers()
