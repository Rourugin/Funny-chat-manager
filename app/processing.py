import re
from datetime import datetime, timedelta

def parse_time(time_string: str | None) -> datetime | None:
    if not time_string:
        return None
    
    match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
    current_datetime = datetime.now()
    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            case "s": time_delta = timedelta(seconds=value)
            case "m": time_delta = timedelta(minutes=value)
            case "h": time_delta = timedelta(hours=value)
            case "d": time_delta = timedelta(days=value)
            case _: return None

    else:
        return None
    new_datetime = current_datetime + time_delta
    return new_datetime