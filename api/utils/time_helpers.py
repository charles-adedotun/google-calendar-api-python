import pytz
from datetime import datetime

def convert_to_timezone(date_str, target_timezone):
    """Converts a datetime string to a target timezone."""
    local_tz = pytz.timezone(target_timezone)
    return datetime.fromisoformat(date_str).astimezone(local_tz).isoformat()

def get_utc_time(date_str):
    """Converts a datetime string to UTC."""
    return datetime.fromisoformat(date_str).astimezone(pytz.UTC).isoformat()
