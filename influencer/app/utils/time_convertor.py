from datetime import datetime, timedelta
# from utils.config import config
from app.config.settings import settings
import pytz
import re

# Setting the timezone
timezone = pytz.timezone(settings.timezone)


def convert_time_to_datetime(time_str: str) -> datetime:
    """
    Convert a time string to a datetime object.

    Args:
        time_str (str): A string representing a time in the format %I:%M %p or %H:%M.

    Returns:
        datetime: A datetime object representing the time on the current date.
    """
    now = datetime.now(timezone)
    # Determine format based on presence of AM/PM
    time_format = "%I:%M %p" if "AM" in time_str or "PM" in time_str else "%H:%M"
    time = datetime.strptime(time_str, time_format).time()
    combined_datetime = datetime.combine(now.date(), time, tzinfo=timezone)

    # if combined_datetime > now:
    #     combined_datetime -= timedelta(days=1)
    return combined_datetime


def convert_weekday_time_to_datetime(weekday_time_str: str) -> datetime:
    """
    Convert a weekday and time string to a datetime object representing the next occurrence of the specified weekday at the specified time.

    Args:
        weekday_time_str (str): A string representing a weekday and time in the format "Weekday, H:M [AM/PM]" or "Weekday, H:M".

    Returns:
        datetime: A datetime object representing the next occurrence of the specified weekday at the specified time.
    """
    weekday_time_str = weekday_time_str.replace(".", "").strip()
    parts = weekday_time_str.split(", ")
    weekday_str, time_str = parts[0], parts[1]

    # Define weekdays and their common abbreviations
    weekdays = {
        "Monday": ["Mon"],
        "Tuesday": ["Tue"],
        "Wednesday": ["Wed"],
        "Thursday": ["Thu"],
        "Friday": ["Fri"],
        "Saturday": ["Sat"],
        "Sunday": ["Sun"],
    }

    # Identify the target weekday by checking each key and its list for a match
    target_weekday = next(
        (
            day_index
            for day_index, (day, abbreviations) in enumerate(weekdays.items())
            if weekday_str == day or weekday_str in abbreviations
        ),
        None,
    )

    now = datetime.now(timezone)
    time_format = "%I:%M %p" if "AM" in time_str or "PM" in time_str else "%H:%M"
    time = datetime.strptime(time_str, time_format).time()
    next_weekday_date = datetime.combine(now.date(), time, tzinfo=timezone)

    # Calculate how many days to subtract to get the last occurrence of the target weekday
    days_to_subtract = (next_weekday_date.weekday() - target_weekday) % 7
    if days_to_subtract == 0 and next_weekday_date.time() > now.time():
        days_to_subtract = (
            7  # If it's today but the time has already passed, go back a full week
        )

    next_weekday_date -= timedelta(days=days_to_subtract)

    return next_weekday_date


def convert_specific_day_to_datetime(day_str: str, time_str: str) -> datetime:
    """
    Convert a specific day string and time string to a datetime object.

    Args:
        day_str (str): A string representing a specific day, e.g. "Yesterday".
        time_str (str): A string representing a time in the format "H:M [AM/PM]" or "H:M".

    Returns:
        datetime: A datetime object representing the specific day and time.
    """
    now = datetime.now(timezone)
    date: datetime
    if "Yesterday" in day_str:
        date = now.date() - timedelta(days=1)
    else:
        raise ValueError("Unsupported relative day string")

    # Determine format based on presence of AM/PM
    time_format: str = "%I:%M %p" if "AM" in time_str or "PM" in time_str else "%H:%M"
    time: time = datetime.strptime(time_str, time_format).time()
    return datetime.combine(date, time, tzinfo=timezone)


def convert_date_to_datetime(date_str: str) -> datetime:
    """
    Convert a date string to a datetime object.

    Args:
        date_str (str): A string representing a date in the format "%b %d %I:%M %p".

    Returns:
        datetime: A datetime object representing the date.
    """
    date_str = re.sub(r"th|rd|nd|st", "", date_str)
    date = datetime.strptime(date_str, "%b %d %I:%M %p")
    now = datetime.now(timezone)

    combined_date = datetime(now.year, date.month, date.day, date.hour, date.minute, tzinfo=timezone)
    if combined_date > now:
        combined_date = datetime(now.year, date.month, date.day, date.hour, date.minute, tzinfo=timezone)
    return combined_date


def convert_relative_time_to_datetime(relative_time_str: str) -> datetime:
    """
    Convert a relative time string to a datetime object.

    Args:
        relative_time_str (str): A string representing a relative time.

    Returns:
        datetime: A datetime object representing the relative time.
    """
    # Check for "Yesterday" pattern
    if "Yesterday" in relative_time_str:
        parts = relative_time_str.split(maxsplit=2)
        day_part, time_part = parts[0], parts[1]
        return convert_specific_day_to_datetime(day_part, time_part)

    # Check for weekday pattern
    if any(
        day in relative_time_str
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    ):
        return convert_weekday_time_to_datetime(relative_time_str)

    # Check for date pattern like "Apr 4th 01:23 AM"
    if re.search(
        r"\bJan\b|\bFeb\b|\bMar\b|\bApr\b|\bMay\b|\bJun\b|\bJul\b|\bAug\b|\bSep\b|\bOct\b|\bNov\b|\bDec\b",
        relative_time_str,
    ):
        return convert_date_to_datetime(relative_time_str)

    # Default to time pattern
    return convert_time_to_datetime(relative_time_str)
