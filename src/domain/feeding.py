import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import setting

conn = sqlite3.connect(f"{setting.ROOT_FOLDER}/{setting.DATABASE_NAME}")
cur = conn.cursor()


@dataclass
class Message:
    volume: float
    created_at: str
    chat_id: int


@dataclass
class Feeding:
    id: Optional[int]
    volume: float
    created_at: str


def create(raw_message: str, chat_id: int) -> Feeding:
    parsed_message: Message = _parse_message(raw_message=raw_message, chat_id=chat_id)
    data: tuple = (
        parsed_message.volume,
        parsed_message.created_at,
        parsed_message.chat_id,
    )
    cur.execute(
        "INSERT INTO feeding (volume, created_at, chat_id) VALUES (?, ?, ?)",
        data,
    )
    conn.commit()

    return Feeding(id=None, volume=parsed_message.volume, created_at=parsed_message.created_at)


def get_list_for_today(chat_id: int) -> List[Feeding]:
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    cur.execute(
        "SELECT * FROM feeding WHERE chat_id=? AND created_at LIKE ? ORDER BY created_at",
        (chat_id, f"%{current_date}%"),
    )

    return [
        Feeding(
            id=row[0],
            created_at=row[1][10:],
            volume=row[2],
        )
        for row in cur.fetchall()
    ]


def in_dates_range(chat_id: int, start_date, end_date) -> list[Feeding]:
    cur.execute(
        "SELECT * FROM feeding WHERE chat_id=? \n"
        "AND DATE(created_at) >= ? AND DATE(created_at) <= ?  ORDER BY created_at",
        (chat_id, start_date, end_date),
    )
    return [
        Feeding(
            id=row[0],
            created_at=row[1][:10],
            volume=row[2],
        )
        for row in cur.fetchall()
    ]


def remove(feed_id: int) -> None:
    try:
        cur.execute("DELETE FROM feeding WHERE id = ?", (feed_id,))
        conn.commit()
    except Exception as e:
        print("Помилка при виконанні SQL-запиту:", e)


def _parse_message(raw_message: str, chat_id: int) -> Message:
    regexp_result = re.match(r"(\d{1,2}:\d{1,2})\s+(\d+(\.\d+)?)", raw_message)
    if regexp_result:
        time = regexp_result.group(1)
        volume = float(regexp_result.group(2))
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        time_obj = datetime.strptime(time, "%H:%M")
        time_formated = time_obj.strftime("%H:%M")
        created_at = f"{current_date} {time_formated}"

        return Message(volume=volume, created_at=created_at, chat_id=chat_id)

    else:
        try:
            volume = float(raw_message)
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            return Message(volume=volume, created_at=created_at, chat_id=chat_id)
        except ValueError:
            return None
