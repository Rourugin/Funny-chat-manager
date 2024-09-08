from typing import Any
from contextlib import suppress
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ChatPermissions, CallbackQuery

import app.database.requests as rq
import app.helpers.processing as pc
import app.database.models as md
import app.keyboards.profile_keyboards as pk


main_router = Router()
main_router.message.filter(F.chat.type == 'supergroup')


@main_router.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    await rq.set_chat(chat_name=message.chat.title, chat_id=message.chat.id)
    await rq.set_user(chat_id=message.chat.id, user_id=message.from_user.id)
    await rq.set_item(chat_id=message.chat.id, user_id=message.from_user.id)
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
        await message.answer(f"Твой провиль: {mention}\n\nЗдоровье: {user.health}❤️\nСчастье: {user.happiness}🎉\nУсталость: {user.fatigue}🥱\nБаланс: {user.money}💰\nКостюм: {user.suit}👙\nНациональность: {user.nation}👽\nГендер: {user.gender}⚧️\nГород: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


@main_router.callback_query(F.data == 'back_profile')
async def back_profile(message: Message) -> Any:
    reply = message.reply_to_message
    if not reply:
        mention = message.from_user.mention_html(message.from_user.first_name)
        user = await rq.get_user(message.from_user.id)
    elif reply:
        mention = reply.from_user.mention_html(reply.from_user.first_name)
        user = await rq.get_user(reply.from_user.id)

    with suppress(TelegramBadRequest):
        await message.answer(f"Твой провиль: {mention}\n\nЗдоровье: {user.health}❤️\nСчастье: {user.happiness}🎉\nУсталость: {user.fatigue}🥱\nБаланс: {user.money}💰\nКостюм: {user.suit}👙\nНациональность: {user.nation}👽\nГендер: {user.gender}⚧️\nГород: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


@main_router.callback_query(F.data == 'food_prof')
async def food_profile(callback: CallbackQuery) -> Any:
    has_scooby_snack = False
    has_five_for_three = False
    item = await rq.get_item(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if item.scooby_snack > 0:
        has_scooby_snack = True
    if item.five_for_threehundred > 0:
        has_five_for_three = True
    if has_scooby_snack == False and has_five_for_three == False:
        await callback.message.answer(f"{mention}, у тебя нет еды", parse_mode="HTML")
    elif has_scooby_snack == True and has_five_for_three == False:
        await callback.message.answer(f"{mention}, твоя жратва:\nСкуби Снэк: {item.scooby_snack}", parse_mode="HTML", reply_markup=pk.eat)
    elif has_scooby_snack == False and has_five_for_three == True:
        await callback.message.answer(f"{mention}, твоя жратва:\n5 за 300: {item.five_for_threehundred}", parse_mode="HTML", reply_markup=pk.eat)
    elif has_scooby_snack == True and has_five_for_three == True:
        await callback.message.answer(f"{mention}, твоя жратва:\nСкуби Снэк: {item.scooby_snack}\n5 за 300: {item.five_for_threehundred}", parse_mode="HTML", reply_markup=pk.eat)
    await callback.answer(None)


@main_router.callback_query(F.data == 'eat_scooby_snack')
async def eat_scooby_snack(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if item.scooby_snack > 0:
        item.scooby_snack -= 1
        user.health += 15
        user.happiness += 15
        user.fatigue -= 15
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer(f"Скуби Снэк был поглошён {mention}", parse_mode="HTML")
    elif item.scooby_snack <= 0:
        await callback.message.answer(f"{mention}, у тебя нет скубиснэков", parse_mode="HTML")
    await callback.answer(None)


@main_router.callback_query(F.data == 'eat_five_for_three')
async def eat_five_for_three(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if item.five_for_threehundred > 0:
        user.health += 69
        user.happiness += 52
        user.fatigue -= 47
        item.five_for_threehundred -= 1
        async with md.async_session() as session:
            await session.merge(user)
            await session.merge(item)
            await session.commit()
        await callback.message.answer(f"5 за 300 был поглошён {mention}", parse_mode="HTML")
    elif item.five_for_threehundred <= 0:
        await callback.message.answer(f"{mention}, у тебя нет 5 за 300", parse_mode="HTML")
    await callback.answer(None)


@main_router.callback_query(F.data == 'clothes_prof')
async def clothes_profile(callback: CallbackQuery) -> Any:
    item = await rq.get_item(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if item.latex_suit == False and item.crusader_suit == False and item.clown_suit == False:
        await callback.message.answer(f"{mention}, у тебя нет одежды", parse_mode="HTML")
    elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == False:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс", parse_mode="HTML", reply_markup=pk.lutex)
    elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == False:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм крестоносца", parse_mode="HTML", reply_markup=pk.crusader)
    elif item.latex_suit == False and item.crusader_suit == False and item.clown_suit == True:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.clown)
    elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == False:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм крестоносца", parse_mode="HTML", reply_markup=pk.lutex_crusader)
    elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == True:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.lutex_clown)
    elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == True:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм крестоносца\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.crusader_clown)
    elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == True:
        await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм крестоносца\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.lutex_crusader_clown)
    await callback.answer(None)


@main_router.callback_query(F.data == 'wear_latex')
async def wear_latex(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    user.suit = "Латексный костюм"
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await callback.answer(None)
    await callback.message.answer("Латексный костюм надет, твоя привлекательность явно выросла")


@main_router.callback_query(F.data == 'wear_crusader')
async def wear_crusader(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    user.suit = "Костюм крестоносца"
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await callback.answer(None)
    await callback.message.answer("Костюм крестоносца надет, пора устраивать поход на священную землю и освобождать её от еретиков!")


@main_router.callback_query(F.data == 'wear_clown')
async def wear_clown(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    user.suit = "Клоунский костюм"
    async with md.async_session() as session:
        await session.merge(user)
        await session.commit()
    await callback.answer(None)
    await callback.message.answer("Клоунский костюм надет, ебать ты, конечно, клоун, хонк-хонк блять!")
