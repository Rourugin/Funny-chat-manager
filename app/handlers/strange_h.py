import os
import random
import asyncio
from typing import Any
from dotenv import load_dotenv
from contextlib import suppress
from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.types import ChatPermissions
from aiogram.exceptions import TelegramBadRequest

import app.database.models as md
import app.database.requests as rq
import app.helpers.processing as pc


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
strange_router = Router()
strange_router.message.filter(F.chat.type == 'supergroup')


@strange_router.message(F.text.lower() == 'glin-dilin')
async def nuclear_war(message: Message) -> Any:
    war_frases = ["Clown in 3 a.m. is attacking!", "Burunya", "Shokonokonokokostantan"]
    await message.answer("⚠️⚠️⚠️NUCLEAR WAR WILL START IN 10 SECONDS⚠️⚠️⚠️")
    await asyncio.sleep(10)
    while True:
        await asyncio.sleep(0.5)
        random_frase = random.choice(war_frases)
        await message.answer(random_frase)


@strange_router.message(F.text.startswith('+gender'))
async def new_gender(message: Message) -> Any:
    gender_space = message.text.find(' ')
    gender = message.text[gender_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.gender = gender
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    if gender.lower() == "clown":
        item = await rq.get_item(message.from_user.id)
        item.clown_suit = True
        async with md.async_session() as session:
            await session.merge(item)
            await session.commit()
        await message.answer("Well, you and the clown, of course, get a suit🤡")
    await message.answer(f"Your new gender is: {user.gender}⚧️")


@strange_router.message(F.text.startswith('+city'))
async def new_city(message: Message) -> Any:
    city_space = message.text.find(' ')
    city = message.text[city_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.city = city
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    if city.lower() == "jerusalem":
        item = await rq.get_item(message.from_user.id)
        item.crusader_suit = True
        async with md.async_session() as session:
            await session.merge(item)
            await session.commit()
        await message.answer("Let's return the Holy Land to the Holy Roman Empire!\nReceived the Crusader costume!")
    await message.answer(f"Your new city is: {user.city}🏙️")


@strange_router.message(F.text.startswith('+nation'))
async def new_nation(message: Message) -> Any:
    nation_space = message.text.find(' ')
    nation = message.text[nation_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.nation = nation
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await message.answer(f"Your new nation is: {user.nation}👽")


@strange_router.message(F.text.lower().contains('stalin'))
async def stalin(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    until_date = pc.parse_time("5m")
    await message.reply("Shoot!")

    with suppress(TelegramBadRequest):
        user.health = 0
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} was shot by I.V. Stalin", parse_mode="HTML")
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))


@strange_router.message(F.text.lower().contains('i love putin'))
async def putin(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)

    with suppress(TelegramBadRequest):
        user.money += 100
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} 100 rubles were transferred to your account from V.V. Putin", parse_mode="HTML")


@strange_router.message(F.text.lower().contains('niggers are sucking') | F.text.lower().contains('niggers suck') | F.text.lower().contains('i am nigger'))
async def nigger(message: Message) -> Any:
    await message.reply("I will cancel you in X (Twitter)")


@strange_router.message(F.text.lower().contains('make america greate again'))
async def greate_america(message: Message) -> Any:
    shot_chance = random.randint(0, 2)
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    if shot_chance == 0:
        user.health = 0
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.reply(f"{mention} was shot, you're not Trump", parse_mode="HTML")
    elif shot_chance > 0:
        user.health -= 5
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention}, today you were lucky, but someone still got shot in the ear", parse_mode="HTML")
