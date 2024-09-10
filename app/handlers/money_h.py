import random
from typing import Any
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import app.database.models as md
import app.database.requests as rq
import app.helpers.processing as pc
import app.keyboards.money_keyboards as mk


money_router = Router()
money_router.message.filter(F.chat.type == 'supergroup')


@money_router.message(Command(commands=['casino']))
async def cmd_casino(message: Message) -> Any:
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    rate_space = message.text.find(' ')
    rate = message.text[rate_space + 1:]
    user.rate = int(rate)
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await message.answer(f"{mention}, хочешь сделать ставку {rate}?", reply_markup=mk.casino_main, parse_mode="HTML")


@money_router.callback_query(F.data == 'play_casino')
async def play_casino(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if int(user.money) < int(user.rate):
        await callback.message.answer(f"{mention}, сходи подзаработай или сдулай ставку приюлежжённую к твоему хую (ну, или Шевцова)", parse_mode="HTML")
    elif int(user.money) >= int(user.rate):
        win_chance = random.randint(0, 10)
        if win_chance <= 2:
            user.money += int(user.rate)
            await callback.message.answer(f"Джекпот, джекпот, хуй {mention} в рот!", reply_markup=mk.casino_main, parse_mode="HTML")
        elif win_chance > 2:
            user.money -= int(user.rate)
            await callback.message.answer(f"{mention}, поцелуй мою залупу, залупу-лупу!", reply_markup=mk.casino_main, parse_mode="HTML")
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
    await callback.answer(None)


@money_router.callback_query(F.data == 'reject_casino')
async def reject_casino(callback: CallbackQuery) -> Any:
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    await callback.message.answer(f"{mention}, ну, ты и ссыкло, конечно, нет чтобы нормально сыграть", parse_mode="HTML")


@money_router.callback_query(F.data == 'info_casino')
async def info_casino(callback: CallbackQuery) -> Any:
    await callback.message.answer(f"При вводе команды /casino введите ставку (не меньше вашего баланса, иначе Вы уйдёте в минус)")
    await callback.answer(None)
