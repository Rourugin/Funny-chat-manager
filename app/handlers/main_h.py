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


@main_router.message(Command(commands=['all_commands']))
async def cmd_all_commands(message: Message) -> Any:
    await message.answer("List of all commands:\n/shop\n/profile\n/casino [bet]\n\nText commands:\npunch\nsuicide\nlick\n\nAdd commands:\n+gender [your_gender]\n+city [your_city]\n+nation [your_nation]")


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
        await message.answer(f"Your profile: {mention}\n\nHealth: {user.health}❤️\nHappiness: {user.happiness}🎉\nFatigue: {user.fatigue}🥱\nBalance: {user.money}💰\nSuit: {user.suit}👙\nNation: {user.nation}👽\nGender: {user.gender}⚧️\nCity: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


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
        await message.answer(f"Your profile: {mention}\n\nHealth: {user.health}❤️\nHappiness: {user.happiness}🎉\nFatigue: {user.fatigue}🥱\nBalance: {user.money}💰\nSuit: {user.suit}👙\nNation: {user.nation}👽\nGender: {user.gender}⚧️\nCity: {user.city}🏙️", parse_mode="HTML", reply_markup=pk.main)


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
        await callback.message.answer(f"{mention}, you have no food", parse_mode="HTML")
    elif has_scooby_snack == True and has_five_for_three == False:
        await callback.message.answer(f"{mention}, your food:\nScooby Snack: {item.scooby_snack}", parse_mode="HTML", reply_markup=pk.eat)
    elif has_scooby_snack == False and has_five_for_three == True:
        await callback.message.answer(f"{mention}, your food:\n5 for 300: {item.five_for_threehundred}", parse_mode="HTML", reply_markup=pk.eat)
    elif has_scooby_snack == True and has_five_for_three == True:
        await callback.message.answer(f"{mention}, your food:\nScooby Snack: {item.scooby_snack}\n5 for 300: {item.five_for_threehundred}", parse_mode="HTML", reply_markup=pk.eat)
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
        await callback.message.answer(f"Scooby Snack was eaten by {mention}", parse_mode="HTML")
    elif item.scooby_snack <= 0:
        await callback.message.answer(f"{mention}, you have no Scooby Snacks", parse_mode="HTML")
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
        await callback.message.answer(f"5 for 300 was eaten by {mention}", parse_mode="HTML")
    elif item.five_for_threehundred <= 0:
        await callback.message.answer(f"{mention}, you have no 5 for 300", parse_mode="HTML")
    await callback.answer(None)


@main_router.callback_query(F.data == 'clothes_prof')
async def clothes_profile(callback: CallbackQuery) -> Any:
    item = await rq.get_item(callback.from_user.id)
    mention = callback.from_user.mention_html(callback.from_user.first_name)
    if item.latex_suit == False and item.crusader_suit == False and item.clown_suit == False:
        await callback.message.answer(f"{mention}, you have no clothes", parse_mode="HTML")
    elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == False:
        await callback.message.answer(f"{mention}, in your wardrobe:\nLatex suit", parse_mode="HTML", reply_markup=pk.latex)
    elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == False:
        await callback.message.answer(f"{mention}, in your wardrobe:\nCrusader suit", parse_mode="HTML", reply_markup=pk.crusader)
    elif item.latex_suit == False and item.crusader_suit == False and item.clown_suit == True:
        await callback.message.answer(f"{mention}, in your wardrobe:\nClown suit", parse_mode="HTML", reply_markup=pk.clown)
    elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == False:
        await callback.message.answer(f"{mention}, in your wardrobe:\nLatex suit\nCrusader suit", parse_mode="HTML", reply_markup=pk.latex_crusader)
    elif item.latex_suit == True and item.crusader_suit == False and item.clown_suit == True:
        await callback.message.answer(f"{mention}, in your wardrobe:\nLatex suit\nClown suit", parse_mode="HTML", reply_markup=pk.latex_clown)
    elif item.latex_suit == False and item.crusader_suit == True and item.clown_suit == True:
        await callback.message.answer(f"{mention}, in your wardrobe:\nCrusader suit\nClown suit", parse_mode="HTML", reply_markup=pk.crusader_clown)
    elif item.latex_suit == True and item.crusader_suit == True and item.clown_suit == True:
        await callback.message.answer(f"{mention}, in your wardrobe:\nLatex suit\nCrusader suit\nClown suit", parse_mode="HTML", reply_markup=pk.latex_crusader_clown)
    await callback.answer(None)


@main_router.callback_query(F.data == 'wear_latex')
async def wear_latex(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.latex_suit == True:
        user.suit = "Latex suit"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.answer(None)
        await callback.message.answer("The latex suit is on, your attractiveness has clearly increased")
    elif item.latex_suit == False:
        await callback.message.answer("You don't have a latex suit")


@main_router.callback_query(F.data == 'wear_crusader')
async def wear_crusader(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.crusader_suit == True:
        user.suit = "Crusader suit"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.answer(None)
        await callback.message.answer("The crusader costume is on, it’s time to organize a campaign on the sacred land and liberate it from heretics!")
    elif item.crusader_suit == False:
        await callback.message.answer("You don't have a crusader costume")


@main_router.callback_query(F.data == 'wear_clown')
async def wear_clown(callback: CallbackQuery) -> Any:
    user = await rq.get_user(callback.from_user.id)
    item = await rq.get_item(callback.from_user.id)
    if item.clown_suit == True:
        user.suit = "Clown suit"
        async with md.async_session() as session:
            await session.merge(user)
            await session.commit()
        await callback.answer(None)
        await callback.message.answer("The clown suit is on, fuck you, of course you are a clown, honk-honk fuck!")
    elif item.clown_suit == False:
        await callback.message.answer("You don't have a clown suit")
