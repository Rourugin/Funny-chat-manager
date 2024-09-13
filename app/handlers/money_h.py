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
    parts = message.text.split()
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    bet = int(parts[1])
    rate = int(parts[2])
    if user.money >= int(rate) * int(bet):
        user.bet = bet
        user.rate = rate
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.reply(f"{mention}, хочешь сделать ставку {rate}?", reply_markup=mk.casino_main, parse_mode="HTML")
    elif user.money < int(rate):
        await message.reply(f"{mention}, у тебя не хватает деняг!", parse_mode="HTML")
    elif user.money < int(rate) * int(bet):
        await message.reply(f"{mention}, у тебя не хватает деняг!", parse_mode="HTML")


@money_router.callback_query(F.data == 'play_casino')
async def play_casino(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
        user = await rq.get_user(callback.from_user.id)
        mention = callback.from_user.mention_html(callback.from_user.first_name)
        if int(user.money) < int(user.rate) * int(user.bet):
            await callback.message.answer(f"{mention}, сходи подзаработай или сдулай ставку приюлежжённую к твоему хую (ну, или Шевцова)", parse_mode="HTML")
        elif int(user.money) >= int(user.rate) * int(user.bet):
            win_chance = random.randint(0, 10)
            if win_chance <= 2:
                user.money += int(user.rate) * int(user.bet)
                await callback.message.answer(f"Джекпот, джекпот, хуй {mention} в рот!", reply_markup=mk.casino_main, parse_mode="HTML")
            elif win_chance > 2:
                user.money -= int(user.rate) * int(user.bet)
                await callback.message.answer(f"{mention}, поцелуй мою залупу, залупу-лупу!", reply_markup=mk.casino_main, parse_mode="HTML")
            async with md.async_session() as session:
                await session.merge(user)
                await session.commit()
        await callback.answer(None)
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Сейчас не твоя игра")


@money_router.callback_query(F.data == 'reject_casino')
async def reject_casino(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
        mention = callback.from_user.mention_html(callback.from_user.first_name)
        await callback.answer(None)
        await callback.message.answer(f"{mention}, ну, ты и ссыкло, конечно, нет чтобы нормально сыграть", parse_mode="HTML")
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Я понимаю, что ты тоже ссышь проиграть, но сейчас выбираешь не ты")


@money_router.callback_query(F.data == 'info_casino')
async def info_casino(callback: CallbackQuery) -> Any:
    await callback.message.answer(f"При вводе команды /casino введите ставку (не меньше вашего баланса, иначе Вы уйдёте в минус)")
    await callback.answer(None)


@money_router.message(F.text.lower().startswith('рулетка'))
async def roulette(message: Message) -> Any:
    parts = message.text.split()
    bet = int(parts[1])
    bullet = int(parts[2])
    user = await rq.get_user(message.from_user.id)
    mention = message.from_user.mention_html(message.from_user.first_name)
    if user.money >= bet * bullet:
        user.bet = bet
        user.rate = bullet
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await message.reply(f"{mention}, хочешь сыграть?", reply_markup=mk.roulette_main, parse_mode="HTML")
    elif user.money < bet * bullet:
        await message.reply(f"{mention}, у тебя не хватает деняг!", parse_mode="HTML")


@money_router.callback_query(F.data == 'play_roulette')
async def play_roulette(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
        user = await rq.get_user(callback.from_user.id)
        mention = callback.from_user.mention_html(callback.from_user.first_name)
        if user.health > 0:
            shoot_chance = random.randint(1, 6)
            if shoot_chance <= user.rate:
                if user.rate == 1:
                    user.money -= user.rate * user.bet
                    await callback.message.answer(f"{mention}, вы проиграли и умерли, ботики!", reply_markup=mk.roulette_main, parse_mode="HTML")
                elif user.rate > 1:
                    if shoot_chance == 1:
                        user.money = 0
                        await callback.message.answer(f"{mention}, вы проиграли и умерли, ботики!\nКстати, вас ещё и обокрали!", reply_markup=mk.roulette_main, parse_mode="HTML")
                    elif shoot_chance > 1:
                        user.money -= user.rate * user.bet
                        await callback.message.answer(f"{mention}, вы проиграли и умерли, ботики!", reply_markup=mk.roulette_main, parse_mode="HTML")
                user.health = 0
            elif shoot_chance > user.bet * user.rate:
                user.money += user.rate * user.bet
                await callback.message.answer(f"{mention}, вы выиграли!", reply_markup=mk.roulette_main, parse_mode="HTML")
            async with md.async_session() as session:
                await session.merge(user)
                await session.commit()
        elif user.health <= 0:
            await callback.message.answer(f"{mention}, тебе бы подлечиться (например пожрать говна)!", parse_mode="HTML")
        await callback.answer(None)
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Если хочешь, стреляй сам")


@money_router.callback_query(F.data == 'reject_roulette')
async def reject_roulette(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
        mention = callback.from_user.mention_html(callback.from_user.first_name)
        await callback.message.answer(f"{mention}, ну, ты и ссыкло, конечно, нет чтобы нормально сыграть, один выстрел и всё", parse_mode="HTML")
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Ссыкло, даже не от своей игры отказываешься")


@money_router.callback_query(F.data == 'info_roulette')
async def info_roulette(callback: CallbackQuery) -> Any:
    await callback.message.answer(f"При вводе команды /roulette введите ставку (не меньше вашего баланса, иначе Вы уйдёте в минус, умноженного на колличество пуль) и колличество пуль в барабане")
    await callback.answer(None)
