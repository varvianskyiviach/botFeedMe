import re

import domain.feeding as feeding
from src.infrastructure.telegram import bot
from src.keyboards.models import CallbackItem
from src.keyboards.service import build_callback_keyboard

global_record_id = None


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
        "🤔 Are you sure? Data cannot be recovered ⁉️",
        reply_markup=build_callback_keyboard(keyboard_patterns),
    )


@bot.callback_query_handler(func=lambda call: call.data in ["confirm", "canceled"])
async def confirmation_delete_record(call):
    global global_record_id
    match call.data:
        case "confirm":
            record_id = global_record_id
            feeding.remove(feed_id=record_id)
            await bot.send_message(
                chat_id=call.message.chat.id,
                text="🔥  Has been removed",
            )
    match call.data:
        case "canceled":
            await bot.send_message(
                chat_id=call.message.chat.id,
                text="❌   Canceled",
            )

    await bot.delete_message(call.message.chat.id, call.message.message_id)
