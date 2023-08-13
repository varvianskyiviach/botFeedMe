from src.domain.analytics import services as analytics_services
from src.domain.dates import services as dates_services
from src.infrastructure.telegram import bot
from src.keyboards.models import CallbackItem
from src.keyboards.service import build_callback_keyboard


async def analytics_general_menu_callback(message):
    keyboard_patterns: list[CallbackItem] = [
        CallbackItem(
            name="7️⃣ Last 7 Days",
            callback_data="Last 7 days",
        ),
        CallbackItem(
            name="⬇️ This month",
            callback_data="This month",
        ),
        CallbackItem(
            name="↪️ Previous month",
            callback_data="Previous month",
        ),
    ]

    await bot.send_message(
        message.chat.id,
        text="🤔 Select the next action",
        reply_markup=build_callback_keyboard(keyboard_patterns),
    )


@bot.callback_query_handler(func=lambda query: query.data in ["Last 7 days", "This month", "Previous month"])
async def analytics_selected_callback(qeury):
    match qeury.data:
        case "Last 7 days":
            start_date, end_date = dates_services.this_month_last_seven_days()

            answer_message = analytics_services.get_basic_analytics_in_range(
                chat_id=qeury.message.chat.id,
                start_date=start_date,
                end_date=end_date,
            )

            await bot.send_message(
                chat_id=qeury.message.chat.id,
                text=answer_message,
                parse_mode="HTML",
            )

        case "This month":
            start_date, end_date = dates_services.this_month_edge_dates()

            answer_message = analytics_services.get_basic_analytics_in_range(
                chat_id=qeury.message.chat.id,
                start_date=start_date,
                end_date=end_date,
            )

            await bot.send_message(
                chat_id=qeury.message.chat.id,
                text=answer_message,
                parse_mode="HTML",
            )

        case "Previous month":
            start_date, end_date = dates_services.previous_month_edge_dates()

            answer_message = analytics_services.get_basic_analytics_in_range(
                chat_id=qeury.message.chat.id,
                start_date=start_date,
                end_date=end_date,
            )

            await bot.send_message(
                chat_id=qeury.message.chat.id,
                text=answer_message,
                parse_mode="HTML",
            )

    await bot.delete_message(qeury.message.chat.id, qeury.message.message_id)
