import os
from typing import Any
from dotenv import load_dotenv
from contextlib import suppress
from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest

import app.database.requests as rq
import app.database.models as md
import app.helpers.processing as pc


light_router = Router()
light_router.message.filter(F.chat.type == 'supergroup')
bot = Bot(token=os.getenv('TOKEN'))


@light_router.message()
async def punch(message: Message) -> Any:
    reply = message.reply_to_message
    if "ударить" in message.text.lower():
        if not reply:
            await message.answer(f"{message.from_user.first_name}, отставить избиение!")
        mention = reply.from_user.mention_html(reply.from_user.first_name)
        user = await rq.get_user(reply.from_user.id)

        with suppress(TelegramBadRequest):
            user.health -= 10
            user.happiness -= 5
            user.fatigue += 3
            await md.async_session().commit()
            await message.answer(f"{message.from_user.first_name} ударил {mention}")
            if user.fatigue >= 100:
                await message.answer(f"{mention} заебался и теперь валяется без возможности двигать всемисвоими мышцами (даже языком)")
                pc.recovery_fatigue(bot=bot, chat_id=message.chat.id, user_id=reply.from_user.id)