import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    volume: float
    created_at: datetime


def _parse_message(raw_message: str) -> Message:
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


print(_parse_message("9:30 150"))
