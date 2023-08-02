import re

import feeding
from src.infrastructure.telegram import bot
from src.keyboards.models import CallbackItem
from src.keyboards.service import build_callback_keyboard
from src.messages import MESSAGES


@bot.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(message.chat.id, MESSAGES["start"])


@bot.message_handler(commands=["help"])
async def help(message):
    await bot.send_message(message.chat.id, MESSAGES["help"])


@bot.message_handler(commands=["add_record"])
async def add_record_command(message):
    await bot.send_message(message.chat.id, MESSAGES["add_record"])


@bot.message_handler(commands=["today"])
async def list_for_today(message):
    feed_list = feeding.get_list_for_today(chat_id=message.chat.id)
    total_volume = sum(feed.volume for feed in feed_list)

    today_list_records = [
        f"{index + 1}. 🍼{feed.volume} ml - 🕒 Time {feed.created_at} 🗑️ /del{index + 1}"
        for index, feed in enumerate(feed_list)
    ]
    answer_message = (
        "Mom, Dad I ate today 👶 \n\n" + "\n\n".join(today_list_records) + "\n\n"
        f"Total volume:  🥛 {total_volume} ml"
    )
    await bot.send_message(message.chat.id, answer_message)


global_record_id = None


@bot.message_handler(func=lambda message: message.text.startswith("/del"))
async def delete_record(message):
    global global_record_id

    match = re.match(r"/del(\d+)(?:@feedings_bot)?", message.text)
    record_number = int(match.group(1))

    feed_list = feeding.get_list_for_today(chat_id=message.chat.id)
    record_id = feed_list[record_number - 1].id
    global_record_id = record_id

    keyboard_patterns: list[CallbackItem] = [
        CallbackItem(
            name="✅  YES",
            callback_data="confirm",
        ),
        CallbackItem(
            name="❌  NO",
            callback_data="canceled",
        ),
    ]

    await bot.send_message(
        message.chat.id,
        "Are you sure? Data cannot be recovered ⁉️",
        reply_markup=build_callback_keyboard(keyboard_patterns),
    )


@bot.callback_query_handler(func=lambda call: True)
async def confirmation_delete_record(call):
    global global_record_id
    if call.data == "confirm":
        record_id = global_record_id
        feeding.remove(feed_id=record_id)
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="🔥  Has been removed",
        )
    elif call.data == "canceled":
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="❌   Canceled",
        )

    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler()
async def add_record(message):
    feed_data = feeding.create(raw_message=message.text, chat_id=message.chat.id)
    answer_message = (
        f"Successful! \n🍼 {feed_data.volume} ml - 🕒 {feed_data.created_at[:5]} "
        f" 📅 {feed_data.created_at[5:]}"
    )

    await bot.send_message(message.chat.id, answer_message)
