"""Examples for datetime, timezone handling, and business date calculations."""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta, timezone
from typing import List


def calculate_age(birth_date: date) -> int:
    """Calculate age in years based on today's date."""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def next_payroll_date(start_date: date, day_of_month: int = 15) -> date:
    """Return the next payroll date on or after the given date."""
    if start_date.day <= day_of_month:
        return date(start_date.year, start_date.month, day_of_month)
    next_month = start_date.month + 1
    year = start_date.year + (next_month - 1) // 12
    month = (next_month - 1) % 12 + 1
    return date(year, month, day_of_month)


def business_days_between(start: date, end: date) -> int:
    """Count business days between two dates inclusive of the start date."""
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


def leave_duration(start: date, end: date) -> int:
    """Return the duration of leave in calendar days."""
    return (end - start).days + 1


def schedule_meeting(day: str, hour: int, minute: int, timezone_name: str = "UTC") -> datetime:
    """Create a timezone-aware meeting datetime."""
    tzinfo = timezone.utc if timezone_name.upper() == "UTC" else timezone(timedelta(hours=5, minutes=30))
    return datetime.strptime(f"{day} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M").replace(tzinfo=tzinfo)


def format_datetime(value: datetime) -> str:
    """Format a datetime as ISO 8601."""
    return value.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(value: str) -> datetime:
    """Parse a datetime string."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def demo() -> List[dict[str, object]]:
    """Print a small set of datetime examples."""
    birth_date = date(1998, 5, 14)
    payroll = next_payroll_date(date(2026, 8, 3))
    meeting = schedule_meeting("2026-08-10", 14, 30)
    results = [
        ("Age", calculate_age(birth_date)),
        ("Next Payroll Date", payroll),
        ("Business Days", business_days_between(date(2026, 8, 1), date(2026, 8, 7))),
        ("Leave Duration", leave_duration(date(2026, 8, 1), date(2026, 8, 5))),
        ("Meeting", format_datetime(meeting)),
        ("Parsed", parse_datetime("2026-08-03 09:00:00")),
    ]
    for name, value in results:
        print(f"{name}: {value}")
    return [{"name": name, "value": value} for name, value in results]


if __name__ == "__main__":
    demo()
