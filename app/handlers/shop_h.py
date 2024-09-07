from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import app.keyboards.shop_keyboards as kb


shop_router = Router()
shop_router.message.filter(F.chat.type == 'supergroup')


@shop_router.message(Command(commands=['shop']))
async def cmd_shop(message: Message) -> Any:
    await message.answer("Добро пожаловать в Магазин! 🛒\n\nдля начала выбери категорию", reply_markup=kb.main)


@shop_router.message(F.data == 'food_shop')
async def food_shop(message: Message) -> Any:
    pass


@shop_router.message(F.data == 'clothes_shop')
async def clothes_shop(message: Message) -> Any:
    pass