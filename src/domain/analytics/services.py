from datetime import datetime

from domain.feeding import Feeding, in_dates_range


def get_basic_analytics_in_range(chat_id, start_date, end_date):
    feeding: list[Feeding] = in_dates_range(
        chat_id,
        start_date,
        end_date,
    )

    volume_for_day: dict[datetime, float] = {}

    for feed in feeding:
        volume_for_day.setdefault(feed.created_at, 0.0)
        volume_for_day[feed.created_at] += float(feed.volume)

    result = [f"📅 {date} - 🍼 Volume - {volume} ml" for date, volume in volume_for_day.items()]

    message_result = (
        "<b>📈 Analytics dates range:</b>\n"
        "**************************\n" + f"<i>{start_date} - {end_date} \n\n</i>" + "\n\n".join(result)
    )

    return message_result
