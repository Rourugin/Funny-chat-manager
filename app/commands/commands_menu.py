from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="shop",
            description="магазин"
        ),
        BotCommand(
            command="profile",
            description="профиль"
        ),
        BotCommand(
            command="all_commands", 
            description="список команд"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())