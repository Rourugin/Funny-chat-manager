from typing import Any
from contextlib import suppress
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatPermissions
from aiogram.filters import CommandStart, Command, CommandObject

import app.database.requests as rq
import app.helpers.processing as pc


main_router = Router()
main_router.message.filter(F.chat.type == 'supergroup')


@main_router.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    await rq.set_chat(chat_name=message.chat.title, chat_id=message.chat.id)
    await rq.set_user(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer("Ну, здарова, Отец!")


@main_router.message(Command(commands=['mute']) or 'мут' in F.text.lower())
async def cmd_mute(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        await message.answer(f"{message.from_user.first_name}, отставить мут!")
    until_date = pc.parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))
        await message.answer(f"{mention} завалил ебальничек!")


@main_router.message(Command(commands=['all_commands']))
async def cmd_all_commands(message: Message) -> Any:
    await message.answer("Вот все команды: /shop\n/profile\n\nА также текстовые команды:\nударить\nсуицид\\самоубийство\\убить себя")

@main_router.message(Command(commands=['profile']))
async def cmd_profile(message: Message) -> Any:
    reply = message.reply_to_message
    if not reply:
        mention = message.from_user.mention_html(message.from_user.first_name)
        user = await rq.get_user(message.from_user.id)
    elif reply:
        mention = reply.from_user.mention_html(reply.from_user.first_name)
        user = await rq.get_user(reply.from_user.id)

    with suppress(TelegramBadRequest):
        await message.answer(f"Твой провиль: {mention}\n\nЗдоровье: {user.health}❤️\nСчастье: {user.happiness}🎉\nУсталость: {user.fatigue}🥱\nБаланс: {user.money}💰\nГендер: {user.gender}⚧️\nГород: {user.city}🏙️", parse_mode="HTML")