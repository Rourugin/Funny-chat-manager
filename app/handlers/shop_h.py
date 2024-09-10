from typing import Any
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import app.database.models as md
import app.database.requests as rq
import app.keyboards.shop_keyboards as kb


shop_router = Router()
shop_router.message.filter(F.chat.type == 'supergroup')


@shop_router.message(Command(commands=['shop']))
async def cmd_shop(message: Message) -> Any:
    await message.answer("Welcome to the Store! 🛒\n\nto begin, select a category", reply_markup=kb.main)


@shop_router.callback_query(F.data == 'back_shop')
async def back_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Welcome to the Store! 🛒\n\nto begin, select a category", reply_markup=kb.main)


@shop_router.callback_query(F.data == 'food_shop')
async def food_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Welcome to the grist of the wild west, we have:\n\nScooby Snack: 15 coins\n5 for 300: three hundred bucks", reply_markup=kb.buy_food)


@shop_router.callback_query(F.data == 'buy_scooby_snack')
async def buy_scooby_snack(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if user.money >= 15:
        user.money -= 15
        item.scooby_snack += 1
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer("Scooby Snack bought!\nAnother one or something else?", reply_markup=kb.buy_food)
    elif user.money < 15:
        await callback.message.answer("Ha ha beggar, snaggle-toothed peasant, go and earn some money")
    await callback.answer(None)


@shop_router.callback_query(F.data == 'buy_five')
async def buy_five(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if user.money >= 300:
        user.money -= 300
        item.five_for_threehundred += 1
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer("I see you are a connoisseur\nBilly is already waiting))", reply_markup=kb.buy_food)
    elif user.money < 300:
        await callback.message.answer("Ha ha beggar, snaggle-toothed peasant, go and earn some money")
    await callback.answer(None)


@shop_router.callback_query(F.data == 'clothes_shop')
async def clothes_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Welcome to M&M the best clothing store in Uryupinsk, you can buy:\n\nLatex suit: 1000 cumcoins", reply_markup=kb.buy_clothes)


@shop_router.callback_query(F.data == 'buy_latex')
async def buy_latex(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if user.money >= 1000:
        user.money -= 1000
        item.latex_suit = True
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer("Oooh, I like this too)\nMeet me at the club)", reply_markup=kb.buy_clothes)
    elif user.money < 1000:
        await callback.message.answer("Sir, it seems that you are just a pathetic semblance of a person, unable to even afford the basic thing.")
    await callback.answer(None)