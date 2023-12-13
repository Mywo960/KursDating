from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import app.database.requests
import keyboard as kb
import aiosqlite
from app.states import Form
import app.database.requests


router = Router()


# Функция для запроса имени при старте
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    await message.answer("Добро пожаловать в бота для знакомств TeleDate!",
                         reply_markup=kb.greeting.as_markup(resize_keyboard=True))
