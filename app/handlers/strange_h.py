import random
import asyncio
from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command


strange_router = Router()
strange_router.message.filter(F.chat.type == 'supergroup')


@strange_router.message(F.text.lower() == 'глинь-дилинь')
async def nuclear_war(message: Message) -> Any:
    war_frases = ["Сосать Америка!", "Burunya", "Shokonokonokokostantan"]
    await message.answer("⚠️⚠️⚠️ЯДЕРНАЯ ВОЙНА НАЧНЁТСЯ ЧЕРЕЗ 10 СЕКУНД⚠️⚠️⚠️")
    await asyncio.sleep(10)
    while True:
        random_frase = random.choice(war_frases)
        await message.answer(random_frase)