import asyncio

from telebot.async_telebot import AsyncTeleBot, types

import feeding
from setting import TELEGRAM_BOT_API_KEY

bot = AsyncTeleBot(TELEGRAM_BOT_API_KEY)


commands_list = [
    types.BotCommand("/start", "start up the bot."),
    types.BotCommand("/help", "get help about commands"),
    types.BotCommand("/today", "get the list of records for today"),
]


@bot.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(
        message.chat.id, "Here you can follow the state of your baby’s feeding"
    )


@bot.message_handler(commands=["today"])
async def list_for_today(message):
    feed_list = feeding.get_list_for_today(chat_id=message.chat.id)
    today_list_records = [
        f"🍼 {feed.volume} ml - Time {feed.created_at}" for feed in feed_list
    ]
    answer_message = "Mom, Dad I ate today 👶 \n\n" + "\n\n".join(today_list_records)
    await bot.send_message(message.chat.id, answer_message)


@bot.message_handler()
async def add_record(message):
    print("sport")
    feed_data = feeding.create(raw_message=message.text, chat_id=message.chat.id)
    answer_message = f"Successful! {feed_data.volume} ml - {feed_data.created_at}"
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
