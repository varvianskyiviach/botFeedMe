import domain.feeding as feeding
from src.application.messages.text import MESSAGES
from src.infrastructure.telegram import bot
from src.keyboards.service import default_keyboard


async def start(message):
    await bot.send_message(message.chat.id, MESSAGES["start"], reply_markup=default_keyboard())


async def help(message):
    await bot.send_message(message.chat.id, MESSAGES["help"])


async def add_record_command(message):
    await bot.send_message(message.chat.id, MESSAGES["add_record"])


async def list_for_today(message):
    feed_list = feeding.get_list_for_today(chat_id=message.chat.id)
    total_volume = sum(feed.volume for feed in feed_list)

    today_list_records = [
        f"{index + 1}. 🍼{feed.volume} ml - 🕒 Time{feed.created_at} 🗑️ /del{index + 1}"
        for index, feed in enumerate(feed_list)
    ]
    answer_message = (
        "Mom, Dad I ate today 👶 \n\n" + "\n\n".join(today_list_records) + "\n\n" f"Total volume:  🥛 {total_volume} ml"
    )
    await bot.send_message(message.chat.id, answer_message)


async def add_record(message):
    feed_data = feeding.create(raw_message=message.text, chat_id=message.chat.id)
    answer_message = (
        f"Successful! \n🍼 {feed_data.volume} ml - 🕒{feed_data.created_at[10:]} " f" 📅 {feed_data.created_at[:10]}"
    )

    await bot.send_message(message.chat.id, answer_message)
