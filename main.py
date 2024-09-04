import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers.__init__ import setup_routers
from app.database.models import async_main
from app.commands.commands_menu import set_commands

async def main() -> None:
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    print("bot is working")
    dp.include_routers(setup_routers())
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot was disabled")