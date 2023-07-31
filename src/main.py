import asyncio

from telebot.async_telebot import AsyncTeleBot, types

import feeding
from setting import TELEGRAM_BOT_API_KEY

bot = AsyncTeleBot(TELEGRAM_BOT_API_KEY)


commands_list = [
    types.BotCommand("/start", "➾ start up the bot;"),
    types.BotCommand("/help", "➾ get help about commands;"),
    types.BotCommand("/today", "➾ get the list of records for today;"),
]


@bot.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(
        message.chat.id,
        "Hello everyone 👋 .  Here you can follow the state of your baby’s feeding. \n\n"
        "My main opportunity is to record a baby’s lunch with data in the database - 🍼 volume, 🕒 time. \n\n"
        "  Just send message in the chat: \n"
        """👉   Format: " time(hh:mm)   volume(number) " or "volume"  '👈\n"""
        "  If you want to save lunch to database. \n\n"
        "Please click command \\help, to get more infromation about my commands. \n\n"
        "Well, my dear parents, it’s time to feed me 😛❗️",
    )


@bot.message_handler(commands=["help"])
async def help(message):
    await bot.send_message(
        message.chat.id,
        "My main opportunity, to get message from the chat and save in database \n" "",
    )


@bot.message_handler(commands=["today"])
async def list_for_today(message):
    feed_list = feeding.get_list_for_today(chat_id=message.chat.id)
    total_volume = sum(feed.volume for feed in feed_list)
    today_list_records = [
        f"🍼 {feed.volume} ml -  🕒 Time {feed.created_at}" for feed in feed_list
    ]
    answer_message = (
        "Mom, Dad I ate today 👶 \n\n" + "\n\n".join(today_list_records) + "\n\n"
        f"Total volume:  {total_volume} ml"
    )
    await bot.send_message(message.chat.id, answer_message)


@bot.message_handler()
async def add_record(message):
    feed_data = feeding.create(raw_message=message.text, chat_id=message.chat.id)
    answer_message = f"Successful! 🍼 {feed_data.volume} ml - 🕒 {feed_data.created_at[:5]  } 📅{feed_data.created_at[5:]}"
    await bot.send_message(message.chat.id, answer_message)


async def set_commands():
    try:
        await bot.set_my_commands(commands_list)
    except Exception as err:
        print(f"Error while setting commands: {err}")


async def start_bot_loop():
    await set_commands()
    while True:
        try:
            await bot.polling(none_stop=True)
        except Exception as err:
            print(f"Polling error: {err}")
            await asyncio.sleep(15)


asyncio.run(start_bot_loop())
