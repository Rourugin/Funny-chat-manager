from typing import Any
from contextlib import suppress
from aiogram import Router, F, Bot
from pymorphy3 import MorphAnalyzer
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatPermissions
from aiogram.filters import CommandStart, Command, CommandObject

import app.database.requests as rq
import app.helpers.processing as pc


main_router = Router()
main_router.message.filter(F.chat.type == 'supergroup')
morch = MorphAnalyzer(lang='ru')
triggers = ["пидор", "скот"]


@main_router.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    await rq.set_chat(chat_name=message.chat.title, chat_id=message.chat.id)
    await rq.set_user(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer("Ну, здарова, Отец!")


@main_router.message(Command(commands=['ban']))
async def cmd_ban(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        await message.answer(f"{message.from_user.first_name}, отставить бан!")
    until_date = pc.parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date)
        await message.answer(f"{mention} пошёл нахуй!")


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


@main_router.message(Command(commands=['shop']))
async def cmd_shop(message: Message) -> Any:
    await message.answer("Тут будет магазин")


@main_router.message(Command(commands=['all_commands']))
async def cmd_all_commands(message: Message) -> Any:
    await message.answer("Вот все команды: /help, /ban, /mute")


@main_router.message(Command(commands=['help']))
async def cmd_help(message: Message) -> Any:
    await message.answer("Что? Тебе нужна помощь?\n\nПопрубуй позвонить 911 хз")
