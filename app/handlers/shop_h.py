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
    await message.answer("Добро пожаловать в Магазин! 🛒\n\nдля начала выбери категорию", reply_markup=kb.main)


@shop_router.callback_query(F.data == 'back_shop')
async def back_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Добро пожаловать в Магазин! 🛒\n\nдля начала выбери категорию", reply_markup=kb.main)


@shop_router.callback_query(F.data == 'food_shop')
async def food_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Добро пожаловать в жральню дикого запада, у нас есть:\n\nСкуби Снэк: 15 денег\n5 за 300: three hundred bucks", reply_markup=kb.buy_food)


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
        await callback.message.answer("Скуби Снэк куплен!\nЕщё один или что-нибудь другое?", reply_markup=kb.buy_food)
    elif user.money < 15:
        await callback.message.answer("Ха-ха нищиеб, кривозубый крестьянин, сходи денег заработай")
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
        await callback.message.answer("Я смотрю вы ценитель\nБилли уже ждёт)", reply_markup=kb.buy_food)
    elif user.money < 300:
        await callback.message.answer("Ха-ха нищиеб, кривозубый крестьянин, сходи денег заработай")
    await callback.answer(None)


@shop_router.callback_query(F.data == 'clothes_shop')
async def clothes_shop(callback: CallbackQuery) -> Any:
    await callback.answer(None)
    await callback.message.answer("Добро пожаловать в M&M самый лучший магазин одежны в Урюпинске, вы можете купить:\n\nЛатексный костюм: 1000 cumcoins", reply_markup=kb.buy_clothes)


@shop_router.callback_query(F.data == 'buy_latex')
async def buy_latex(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if user.money >= 1000:
        user.money -= 1000
        item.lutex_suit = True
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer("О-о-о, мне тоже такое нравится)\nВстретимся в клубе)", reply_markup=kb.buy_clothes)
    elif user.money < 1000:
        await callback.message.answer("Сэр, сюдя по всему вы лишь жалкое подобие человека, неспособное даже позволить себе базовую вещь.")
    await callback.answer(None)