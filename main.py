import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from config import TOKEN
import app.pref
import app.handler
import app.questionarie
import app.finding

bot = Bot(token=TOKEN, parse_mode="HTML")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(app.handler.router, app.finding.router, app.pref.router, app.questionarie.router)
    await dp.start_polling(bot)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
