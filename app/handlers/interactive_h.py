import os
import tracemalloc
from typing import Any
from dotenv import load_dotenv
from contextlib import suppress
from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest

import app.database.models as md
import app.database.requests as rq
import app.helpers.processing as pc


load_dotenv()
tracemalloc.start()
interactive_router = Router()
interactive_router.message.filter(F.chat.type == 'supergroup')
bot = Bot(token=os.getenv('TOKEN'))


@interactive_router.message(F.text.lower() == 'ударить')
async def punch(message: Message) -> Any:
    reply = message.reply_to_message
    if not reply:
        await message.answer(f"{message.from_user.first_name}, отставить избиение!")
    mention_first = message.from_user.mention_html(message.from_user.first_name)
    mention_second = reply.from_user.mention_html(reply.from_user.first_name)
    user = await rq.get_user(reply.from_user.id)

    with suppress(TelegramBadRequest):
        if user.health >= 0:
            user.health -= 10
        elif user.health < 0:
            user.health = 0
        if user.suit == "Латексный костюм":
            user.happiness += 5
            await message.answer(f"Блягодаря латексному костюму {mention_second} получил удовольствие", parse_mode="HTML")
        elif user.suit != "Латексный костюм":
            if user.happiness >= 0:
                user.happiness -= 5
            elif user.happiness < 0:
                user.happiness = 0
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention_first} ударил {mention_second}", parse_mode="HTML")
        await pc.death(health=user.health, message=message, mention=mention_second, bot=bot, chat_id=message.chat.id, user_id=reply.from_user.id)
        await pc.check_fatigue(fatigue=user.fatigue, message=message, mention=mention_second, bot=bot, chat_id=message.chat.id, user_id=reply.from_user.id)


@interactive_router.message(lambda message: any(phrase in message.text for phrase in ['убить себя', 'самоубийство', 'суицид']))
async def kill_yourself(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)

    with suppress(TelegramBadRequest):
        user.health = 0
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} захуярил себя!", parse_mode="HTML")


@interactive_router.message(lambda message: any(phrase in message.text for phrase in ['лизь', 'лизнуть']))
async def lick(message: Message) -> Any:
    reply = message.reply_to_message
    mention_first = message.from_user.mention_html(message.from_user.first_name)
    if not reply:
        await message.answer(f"{mention_first}, нельзя лизать самого себя!")
    mention_second = reply.from_user.mention_html(reply.from_user.first_name)
    user = await rq.get_user(reply.from_user.id)

    with suppress(TelegramBadRequest):
        if user.suit == "Латексный костюм":
            user.happiness += 15
        elif user.suit != "Латексный костюм":
            user.happiness += 2
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention_first} лизнул {mention_second}", parse_mode="HTML")
        await pc.check_fatigue(fatigue=user.fatigue, message=message, mention=mention_second, bot=bot, chat_id=message.chat.id, user_id=reply.from_user.id)
