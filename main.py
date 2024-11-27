from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from bot_config import database
from handlers.hw_dialog import hw_router

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

import asyncio
from handlers.start import start_router

async def on_startup(bot):
    await bot.send_message(chat_id=1629085599,text="Я онлайн")
    database.create_tables()

async def main():
    dp.include_router(start_router)
    dp.startup.register(on_startup)
    dp.include_router(hw_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())