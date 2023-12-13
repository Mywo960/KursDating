from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import app.database.requests
import keyboard as kb
import aiosqlite
from app.states import *
import app.database.requests
from main import bot

router = Router()


@router.message(Command("Просмотр_анкет"))
async def start_finding(message: types.Message, state: FSMContext):
    if await app.database.requests.is_pref_registered(message.from_user.id):
        if await app.database.requests.is_user_registered(message.from_user.id):
            await message.answer("Начинаем поиск")
            global user_data

            user_data = await app.database.requests.get_users_data_except_me(message.from_user.id)
            print(user_data)
            print(len(user_data))
            await state.set_state(Finding.stat)
            await state.update_data(num=0)
            await state.update_data(people=user_data)

            num = await state.get_data()
            print(num.get('people'))
            formatted_text = []
            photo_file_id = user_data[num.get('num')][-1]
            formatted_text.append(f"Имя: {user_data[num.get('num')][2]}\n"
                                  f"Пол: {user_data[num.get('num')][4]}\n"
                                  f"Возраст: {user_data[num.get('num')][5]}\n"
                                  f"Город: {user_data[num.get('num')][3]}\n"
                                  f"О себе: {user_data[num.get('num')][6]}\n"
                                  # f'Tg: <a href="tg://user?id={user_data[num.get("num")][1]}"> Профиль </a>\n'
                                  )
            await message.answer_photo(
                photo_file_id,
                "\n".join(formatted_text), reply_markup=kb.is_like.as_markup(resize_keyboard=True))


            await state.set_state(Finding.finding)
        else:
            await message.answer("Вы не заполнили анкету", reply_markup=kb.greeting.as_markup(resize_keyboard=True))

    else:
        await message.answer("Вы не ввелм предпочтения", reply_markup=kb.greeting.as_markup(resize_keyboard=True))



@router.message(Finding.finding, F.text == '❤️')
async def like(message: types.Message, state: FSMContext):
    data = await state.get_data()

    my_data = await app.database.requests.get_user_data(message.from_user.id)
    await app.database.requests.set_matches_like(message.from_user.id, data.get('people')[data.get('num')][1])

    formatted_text = []
    photo_file_id = my_data[-1]
    formatted_text.append(f"Имя: {my_data[2]}\n"
                          f"Пол: {my_data[4]}\n"
                          f"Возраст: {my_data[5]}\n"
                          f"Город: {my_data[3]}\n"
                          f"О себе: {my_data[6]}\n"
                          f'Tg: <a href="tg://user?id={my_data[1]}"> Профиль </a>\n'
                          )

    await bot.send_message(chat_id=data.get('people')[data.get('num')][1], text="Вам поставили лайк", reply_markup=kb.greeting.as_markup(resize_keyboard=True))

    await bot.send_photo(chat_id=data.get('people')[data.get('num')][1], photo=photo_file_id, caption="\n".join(formatted_text))


    new_num = data.get('num') + 1
    await state.update_data(num=new_num)
    num = await state.get_data()
    if num.get('num') < len(num.get('people')):
        formatted_text = []
        photo_file_id = num.get('people')[num.get('num')][-1]
        formatted_text.append(f"Имя: {num.get('people')[num.get('num')][2]}\n"
                              f"Пол: {num.get('people')[num.get('num')][4]}\n"
                              f"Возраст: {num.get('people')[num.get('num')][5]}\n"
                              f"Город: {num.get('people')[num.get('num')][3]}\n"
                              f"О себе: {num.get('people')[num.get('num')][6]}\n"
                              # f'Tg: <a href="tg://user?id={num.get('people')[num.get("num")][1]}"> Профиль </a>\n'
                              )
        await message.answer_photo(
            photo_file_id,
            "\n".join(formatted_text), reply_markup=kb.is_like.as_markup(resize_keyboard=True))
    else:
        await message.answer("Анкеты закончились", reply_markup=kb.greeting.as_markup(resize_keyboard=True))
        await state.clear()


@router.message(Finding.finding, F.text == '👎')
async def dislike(message: types.Message, state: FSMContext):
    num = await state.get_data()

    # await bot.send_message(chat_id=num.get('people')[num.get('num')][1], text="Вам поставили лайк", reply_markup=kb.get_like.as_markup(resize_keyboard=True))
    new_num = num.get('num') + 1
    await state.update_data(num=new_num)
    num = await state.get_data()
    if num.get('num') < len(num.get('people')):
        formatted_text = []
        photo_file_id = num.get('people')[num.get('num')][-1]
        formatted_text.append(f"Имя: {num.get('people')[num.get('num')][2]}\n"
                              f"Пол: {num.get('people')[num.get('num')][4]}\n"
                              f"Возраст: {num.get('people')[num.get('num')][5]}\n"
                              f"Город: {num.get('people')[num.get('num')][3]}\n"
                              f"О себе: {num.get('people')[num.get('num')][6]}\n"
                              # f'Tg: <a href="tg://user?id={user_data[num.get("num")][1]}"> Профиль </a>\n'
                              )
        await message.answer_photo(
            photo_file_id,
            "\n".join(formatted_text), reply_markup=kb.is_like.as_markup(resize_keyboard=True))
    else:
        await message.answer("Анкеты закончились", reply_markup=kb.greeting.as_markup(resize_keyboard=True))
        await state.clear()

