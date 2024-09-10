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
    await message.answer(f"{mention}, want to place a bet {rate}?", reply_markup=mk.casino_main, parse_mode="HTML")


@money_router.callback_query(F.data == 'play_casino')
async def play_casino(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if int(user.money) < int(user.rate):
        await callback.message.answer(f"{mention}, go make some money or cheat the bet attached to your dick (ну, или Шевцова)", parse_mode="HTML")
    elif int(user.money) >= int(user.rate):
        win_chance = random.randint(0, 10)
        if win_chance <= 2:
            user.money += int(user.rate)
            await callback.message.answer(f"Jackpot, jackpot, dick in {mention}' mouth!", reply_markup=mk.casino_main, parse_mode="HTML")
        elif win_chance > 2:
            user.money -= int(user.rate)
            await callback.message.answer(f"{mention}, kiss my ass, my ass!", reply_markup=mk.casino_main, parse_mode="HTML")
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
    await callback.answer(None)


@money_router.callback_query(F.data == 'reject_casino')
async def reject_casino(callback: CallbackQuery) -> Any:
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    await callback.message.answer(f"{mention}, well, you're a piss, not to play normally", parse_mode="HTML")


@money_router.callback_query(F.data == 'info_casino')
async def info_casino(callback: CallbackQuery) -> Any:
    await callback.message.answer(f"When entering the /casino command, enter a bet (not less than your balance, otherwise you will go into the red)")
    await callback.answer(None)
