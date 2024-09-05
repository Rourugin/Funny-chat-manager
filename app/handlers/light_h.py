from typing import Any
from aiogram import Router, F
from contextlib import suppress
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

import app.database.requests as rq


light_router = Router()
light_router.message.filter(F.chat.type == 'supergroup')


@light_router.message()
async def punch(message: Message) -> Any:
    reply = message.reply_to_message
    if "ударить" in message.text.lower():
        if not reply:
            await message.answer(f"{message.from_user.first_name}, отставить избиение!")
        mention = reply.from_user.mention_html(reply.from_user.first_name)
        stats = rq.get_user(reply.from_user.id)

        with suppress(TelegramBadRequest):
            await message.answer(f"{message.from_user.first_name} ударил {mention}")