from typing import Any
from contextlib import suppress
from aiogram import Router, F, Bot
from pymorphy3 import MorphAnalyzer
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatPermissions
from aiogram.filters import CommandStart, Command, CommandObject

import app.database.requests as rq
import app.processing as pc


router = Router()
router.message.filter(F.chat.type == 'supergroup', F.from_user.id == 5604550432)
morch = MorphAnalyzer(lang='ru')
triggers = ["пидор", "скот"]


@router.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    #await rq.set_user(chat_name=message.chat.username, chat_id=message.chat.id)
    await message.answer("Ну, здарова, Отец!")


@router.message(Command(commands=['ban']))
async def cmd_ban(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        await message.answer(f"{message.from_user.first_name}, отставить бан!")
    until_date = pc.parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date)
        await message.answer(f"{mention} пошёл нахуй!")


@router.message(Command(commands=['mute']))
async def cmd_mute(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
    reply = message.reply_to_message
    if not reply:
        await message.answer(f"{message.from_user.first_name}, отставить мут!")
    until_date = pc.parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date, permissions=ChatPermissions(can_send_messages=False))
        await message.answer(f"{mention} завалил ебальничек!")


@router.message(Command(commands=['help']))
async def cmd_help(message: Message) -> Any:
    await message.answer('Help!')


@router.message(Command(commands=['all_commands']))
async def cmd_all_commands(message: Message) -> Any:
    await message.answer('All commands!')


@router.message(F.text)
async def profinity_filter(message: Message) -> Any:
    for word in message.text.lower().strip().split():
        parsed_morph = morch.parse(word)[0]
        normal_form = parsed_morph.normal_form

        for trigger in triggers:
            if trigger in normal_form:
                return await message.reply("Сам такой, сучара")