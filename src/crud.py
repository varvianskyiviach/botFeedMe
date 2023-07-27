import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime

import setting

conn = sqlite3.connect(f"{setting.ROOT_FOLDER}/{setting.DATABASE_NAME}")
cur = conn.cursor()

# cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', user_data)
# print(f"{setting.ROOT_FOLDER}/{setting.DATABASE_NAME}")


@dataclass
class Message:
    volume: float
    created_at: datetime
    # chat_id: int


@dataclass
class Feeding:
    volume: float
    created_at: datetime


def create(raw_message: str) -> Feeding:
    parsed_message: Message = _parse_message(raw_message)
    data: tuple = (parsed_message.volume, parsed_message.created_at)
    cur.execute(
        "INSERT INTO feeding (volume, created_at) VALUES (?, ?)",
        data,
    )
    conn.commit()

    return Feeding(volume=parsed_message.volume, created_at=parsed_message.created_at)


def _parse_message(raw_message: str) -> Message:
    # chat_id = raw_message.chat_id()
    regexp_result = re.match(r"(\d{1,2}:\d{1,2})\s+(\d+(\.\d+)?)", raw_message)
    current_time = datetime.now()
    if regexp_result:
        time = regexp_result.group(1)
        volume = float(regexp_result.group(2))

        current_date = current_time.date()
        time_with_date = f"{current_date} {time}"
        created_at = datetime.strptime(time_with_date, "%Y-%m-%d %H:%M")

        return Message(volume=volume, created_at=created_at)

    else:
        volume = re.match(r"(\d+(\.\d+)?)", raw_message)
        if volume:
            volume = float(volume.group(1))
            created_at = current_time
            return Message(volume=volume, created_at=created_at)
        else:
            return None
