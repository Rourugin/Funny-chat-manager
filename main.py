import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

import app.main_handlers as mh
import app.light_handlers as lh
from app.database.models import async_main
from app.commands_menu import set_commands

async def main() -> None:
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    print("bot is working")
    dp.include_router(mh.router)
    #dp.include_router(lh.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot was disabled")