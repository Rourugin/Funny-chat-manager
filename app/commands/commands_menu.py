from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="help", 
            description="information about bot"
            ),
        BotCommand(
            command="all_commands", 
            description="all commands list"
            )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())