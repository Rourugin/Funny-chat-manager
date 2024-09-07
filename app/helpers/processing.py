import re
from typing import Any
from aiogram import Bot
from aiogram.types import Message
from datetime import datetime, timedelta
from aiogram.types import ChatPermissions


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


async def check_fatigue(fatigue: int, message: Message, mention: str, bot: Bot, chat_id: int, user_id: int) -> Any:
    if fatigue >= 100:
        until_date = parse_time("5m")
        await message.answer(f"{mention} заебался и теперь валяется без возможности двигать всеми своими мышцами (даже языком)")
        await bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))