from typing import Any
from contextlib import suppress
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.database.requests as rq
import app.database.models as md
import app.keyboards.profile_keyboards as pk


main_router = Router()
main_router.message.filter(F.chat.type == 'supergroup')
person_id = None


@main_router.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    await rq.set_chat(chat_name=message.chat.title, chat_id=message.chat.id)
    await rq.set_user(chat_id=message.chat.id, user_id=message.from_user.id)
    await rq.set_item(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer("Ну, здарова, Отец!")


@main_router.message(Command(commands=['all_commands']))
async def cmd_all_commands(message: Message) -> Any:
    await message.answer("Список всех команд:\n/shop\n/profile\n/casino [ставка]\n\nТекстовые команды:\nударить\nсуицид\\самоубийство\\убить себя\nлизб\\лизнуть\nрулетка [ставка] [пули в барабане]\n\nИнформационные команды:\n+гендер [твой гендер]\n+город [твой город]\n+нация\\+национальность [твоя национальность]")


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
                await message.reply(f"Твой провиль: {mention}\n\nЗдоровье: {user.health}❤️\nСчастье: {user.happiness}🎉\nУсталость: {user.fatigue}🥱\nБаланс: {user.money}💰\nКостюм: {user.suit}👙\nНациональность: {user.nation}👽\nГендер: {user.gender}⚧️\nГород: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


@main_router.callback_query(F.data == 'back_profile')
async def back_profile(callback: Message) -> Any:
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    user = await rq.get_user(callback.from_user.id)

    with suppress(TelegramBadRequest):
        await callback.answer(None)
        await callback.message.reply(text=f"Твой провиль: {mention}\n\nЗдоровье: {user.health}❤️\nСчастье: {user.happiness}🎉\nУсталость: {user.fatigue}🥱\nБаланс: {user.money}💰\nКостюм: {user.suit}👙\nНациональность: {user.nation}👽\nГендер: {user.gender}⚧️\nГород: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


@main_router.callback_query(F.data == 'food_prof')
async def food_profile(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
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
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Эта кнопка НЕ. ДЛЯ. ТЕБЯ.")


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
    reply = callback.message.reply_to_message
    if reply.from_user.id == callback.from_user.id:
        item = await rq.get_item(callback.from_user.id)
        mention = callback.from_user.mention_html(callback.from_user.first_name)
        if item.latex_suit == False and item.crusader_suit == False and item.clown_suit == False:
            await callback.message.answer(f"{mention}, у тебя нет одежды", parse_mode="HTML")
        elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == False:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс", parse_mode="HTML", reply_markup=pk.latex)
        elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == False:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм крестоносца", parse_mode="HTML", reply_markup=pk.crusader)
        elif item.latex_suit == False and item.crusader_suit == False and item.clown_suit == True:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.clown)
        elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == False:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм крестоносца", parse_mode="HTML", reply_markup=pk.latex_crusader)
        elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == True:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.latex_clown)
        elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == True:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nКостюм крестоносца\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.crusader_clown)
        elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == True:
            await callback.message.answer(f"{mention}, в твоём гардеробе:\nЛатекс\nКостюм крестоносца\nКостюм клоуна", parse_mode="HTML", reply_markup=pk.latex_crusader_clown)
        await callback.answer(None)
    elif reply.from_user.id != callback.from_user.id:
        await callback.answer("Эта кнопоска не для тебя цвела")


@main_router.callback_query(F.data == 'wear_latex')
async def wear_latex(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.latex_suit == True:
        user.suit = "Латексный костюм"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.message.answer("Латексный костюм надет, твоя привлекательность явно выросла")
    elif item.latex_suit == False:
        await callback.message.answer("У тебя нет латексного костюма")
    await callback.answer(None)


@main_router.callback_query(F.data == 'wear_crusader')
async def wear_crusader(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.crusader_suit == True:
        user.suit = "Костюм крестоносца"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.message.answer("Костюм крестоносца надет, пора устраивать поход на священную землю и освобождать её от еретиков!")
    elif item.crusader_suit == False:
        await callback.message.answer("У тебя нет костюма крестоносца")
    await callback.answer(None)


@main_router.callback_query(F.data == 'wear_clown')
async def wear_clown(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.clown_suit == True:
        user.suit = "Клоунский костюм"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.message.answer("Клоунский костюм надет, ебать ты, конечно, клоун, хонк-хонк блять!")
    elif item.clown_suit == False:
        await callback.message.answer("У тебя нет костюма клоуна")
    await callback.answer(None)


@main_router.message(F.text == 'коллбэк')
async def check_callback(message: Message):
    await message.reply("test callback button", reply_markup=pk.test_callback)


@main_router.callback_query(F.data == 'callback_test')
async def callback_test(callback: CallbackQuery) -> Any:
    reply = callback.message.reply_to_message
    await callback.answer(None)
    await callback.message.answer(f"{callback.from_user.id} || {reply.from_user.id}")