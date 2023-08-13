import calendar
from datetime import date, timedelta
from functools import partial


def month_dates_range(year: int, month: int) -> tuple[date, date]:
    _month = partial(date, year=year, month=month)
    _, last_day = calendar.monthrange(year, month)

    first_date = _month(day=1)
    last_date = _month(day=last_day)

    return first_date, last_date


def this_month_edge_dates() -> tuple[date, date]:
    """Returns the first and last date in current month."""

    today = date.today()
    return month_dates_range(year=today.year, month=today.month)


def previous_month_edge_dates() -> tuple[date, date]:
    """Returns the first and last date in previous month."""

    prev_month_day = date.today() - timedelta(weeks=4)
    return month_dates_range(year=prev_month_day.year, month=prev_month_day.month)


def this_month_last_seven_days() -> tuple[date, date]:
    """Return the last 7 days from current day"""

    today = date.today()
    prev_seven_day = today - timedelta(days=6)

    return prev_seven_day, today
