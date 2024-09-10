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


@strange_router.message(F.text.lower() == 'глинь-дилинь')
async def nuclear_war(message: Message) -> Any:
    war_frases = ["Сосать Америка!", "Burunya", "Shokonokonokokostantan"]
    await message.answer("⚠️⚠️⚠️ЯДЕРНАЯ ВОЙНА НАЧНЁТСЯ ЧЕРЕЗ 10 СЕКУНД⚠️⚠️⚠️")
    await asyncio.sleep(10)
    while True:
        await asyncio.sleep(0.5)
        random_frase = random.choice(war_frases)
        await message.answer(random_frase)


@strange_router.message(F.text.startswith('+гендер'))
async def new_gender(message: Message) -> Any:
    gender_space = message.text.find(' ')
    gender = message.text[gender_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.gender = gender
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    if gender.lower() == "клоун":
        item = await rq.get_item(message.from_user.id)
        item.clown_suit = True
        async with md.async_session() as session:
            await session.merge(item)
            await session.commit()
        await message.answer("Ну, ты и клоун, конечно, лови костюм🤡")
    await message.answer(f"Твой гендер: {user.gender}⚧️")


@strange_router.message(F.text.startswith('+город'))
async def new_city(message: Message) -> Any:
    city_space = message.text.find(' ')
    city = message.text[city_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.city = city
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    if city.lower() == "иерусалим":
        item = await rq.get_item(message.from_user.id)
        item.crusader_suit = True
        async with md.async_session() as session:
            await session.merge(item)
            await session.commit()
        await message.answer("Вернём Священную землю Священной Римской Империи!\nПолучен костюм крестоносца!")
    await message.answer(f"Твой город: {user.city}🏙️")


@strange_router.message(F.text.startswith('+национальность') | F.text.startswith('+нация'))
async def new_nation(message: Message) -> Any:
    nation_space = message.text.find(' ')
    nation = message.text[nation_space + 1:]
    user = await rq.get_user(message.from_user.id)
    user.nation = nation
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await message.answer(f"Твоя национальность: {user.nation}👽")


@strange_router.message(F.text.lower().contains('сталин'))
async def stalin(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    until_date = pc.parse_time("5m")
    await message.reply("Расстрелять!")

    with suppress(TelegramBadRequest):
        user.health = 0
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} был расстрелен И. В. Сталином", parse_mode="HTML")
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))


@strange_router.message(F.text.lower().contains('гитлер'))
async def hitler(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    until_date = pc.parse_time("5m")
    if (user.nation == 'еврей') or (user.nation == 'Еврей'):
        await message.reply("В газовую камеру еврея!")

        with suppress(TelegramBadRequest):
            user.health = 0
            async with md.async_session() as session:
                await session.merge(user)
                await session.commit()
            await message.answer(f"{mention} сдох в газовой камере, не буди лихо, пока оно тихо", parse_mode="HTML")
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))


@strange_router.message(F.text.lower().contains('я люблю путина'))
async def putin(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)

    with suppress(TelegramBadRequest):
        user.money += 100
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} вам на счёт переведено 100 рублей от В. В. Путиин", parse_mode="HTML")


@strange_router.message(F.text.lower().contains('шевцов'))
async def schevtsov(message: Message) -> Any:
    await message.reply("Это самое маленькое сообщение, что я видел в своей жизни")


@strange_router.message(F.text.lower().contains('niggers are sucking') | F.text.lower().contains('niggers suck') | F.text.lower().contains('i am nigger'))
async def nigger(message: Message) -> Any:
    await message.reply("Будь мы в worns of armogedon, я бы тебя забанил, но сегодня дебе повезло")


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
        await message.reply(f"{mention} был застрелен, ты ж не Трамп ей богу", parse_mode="HTML")
    elif shot_chance > 0:
        user.health -= 5
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.answer(f"{mention} сегодня тебе повезло, однако кому-то всё же прострелили ухо", parse_mode="HTML")


@strange_router.message(F.text.lower().contains('некоарк только для приколов'))
async def nekocark(message: Message) -> Any:
    await message.answer("–Ты случаем не из этих, которые НекоАрк любит?\n" + 
"–Конечно нет. Я бы никогда не подумал о том, чтобы раздеть НекоАрк и облизать еë худенькое тело, покусывая шею и целуя еë очаровательные маленькие сосочки. Только бессердечный монстр может подумать о еë милом девичьем ротике и язычке, охватывающих толстый член, скользкий от еë слюны и двигающийся в еë рту, пока не наступит эякуляция столь обильная, что еë маленькое горло не сможет проглотить столько.\n" + 
"Сама мысль о густой сперме, переполняющей еë рот, стекающей с еë щёчек на плоскую грудь, еë тонких ручках, зачëрпывающих еë и слизывающих с кончиков пальцев просто ужасна. Вы просто сборище больных извращенцев, думающих о том, чтобы раздвинуть еë стройные бëдра, направив член на еë чистую, узкую девственную щëлку и войти в неë так глубоко, что только стон сорвëтся с еë губ, липких от спермы, пока еë маленькое тело дрожит от того, что еë невинность порвали одним быстрым движением.\n" +
"Мне отвратительно думать о том, что вы ещё больше возбуждаетесь налегая на неë, слушая еë ускоренное дыхание, еë девичьи стоны и придыхания, пока вы ускоряете движение, еë сладкое дыхание, тëплое и влажное, в ваше лицо, и еë плоскую грудь, блестящую от капель свежего пота, быстро вздымающуюся и падающую, чтобы встретиться с вашей.\n" +
"Это на самом деле омерзительно, как вы ощупываете всë еë тело, пока насилуете еë, чувствуя еë сосочки, твердеющие под вашим языком, пока вы лижете еë грудь, еë шею и еë подмышки, чувствуюте вкус еë кожи и пота, пока она дрожит от стимуляции, и доводите еë до оргазма, слушая еë мягкий крик первого оргазма, пока ваш член находится глубоко внутри неë, дико пульсируя, выплëскивая огромное количество горячей спермы, рвущейся вперёд и вытекающей впервые из еë только что осквернëнной вагины, заполняя еë матку, только чтобы вылиться из неë с противным хлюпаньем.\n")
