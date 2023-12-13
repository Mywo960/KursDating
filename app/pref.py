from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import app.database.requests
import keyboard as kb
import aiosqlite
import app.database.requests
from app.states import *

router = Router()

@router.message(Command("Предпочтения"))
async def pef(message: types.Message, state: FSMContext):
    if await app.database.requests.is_pref_registered(message.from_user.id):

        data = await app.database.requests.get_pref_data(message.from_user.id)
        await message.answer("Вот ваши предпочтения", reply_markup=kb.my_pref.as_markup(resize_keyboard=True))
        formatted_text = []
        formatted_text.append(f"Пол: {data[2]}\n"
                              f"Минимальный возраст: {data[3]}\n"
                              f"Максимальный возраст: {data[4]}\n"
                              )
        await message.answer(''.join(formatted_text))


    else:
        await state.set_state(Preferences.gender)
        await message.answer("У вса пока нет предпочтений. Для начала выберите пол в предпочтениях", reply_markup=kb.gender.as_markup(resize_keyboard=True))

@router.message(Command("Удалить_предпочтения"))
async def again_pref(message: types.Message, state: FSMContext):
    await app.database.requests.del_pref_data(message.from_user.id)
    await message.answer("Предпочтения успешно удалены!", reply_markup=kb.greeting.as_markup(resize_keyboard=True))


@router.message(Command("Заполнить_предпочтения_заново"))
async def again_pref(message: types.Message, state: FSMContext):
    await app.database.requests.del_pref_data(message.from_user.id)
    await state.set_state(Preferences.gender)
    await message.answer("Для начала выберите пол в предпочтениях", reply_markup=kb.gender.as_markup(resize_keyboard=True))


@router.message(Preferences.gender, F.text.casefold().in_(["парень", "девушка"]))
async def pref_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Preferences.age_min)
    await message.answer("Укажите минимальный возраст(минимум 16)")

@router.message(Preferences.gender)
async def pref_gender_incorrect(message: types.Message, state: FSMContext):
    await message.answer("Нажмите на кнопку", reply_markup=kb.gender.as_markup(resize_keyboard=True, one_time_keyboard=True))



@router.message(Preferences.age_min)
async def pref_age_min(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 60:
        global age_min
        age_min = int(message.text)
        await state.update_data(age_min=message.text)
        await state.set_state(Preferences.age_max)
        await message.answer(f"Минимальный возраст -{message.text} лет. Теперь давай определимся с максимальным(не более 60).")
    else:
        await message.answer("Вы неправильно ввели число или число меньше 16")


@router.message(Preferences.age_max)
async def pref_age_max(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 60 and int(message.text) >= age_min:
        await state.update_data(age_max=message.text)

        await message.answer(f"Максимальный возраст -{message.text} лет.")
        data = await state.get_data()
        formatted_text = []

        formatted_text.append(f"Пол: {data.get('gender')}\n"
                              f"Минимальный возраст: {data.get('age_min')}\n"
                              f"Максимальный возраст: {data.get('age_max')}\n"
                              )
        await message.answer(''.join(formatted_text))
        await message.answer("Сохранить предпочтения?", reply_markup=kb.chooseb.as_markup(resize_keyboard=True, one_time_keyboard=True))
        await state.set_state(Preferences.choose)
    else:
        await message.answer("Вы неправильно ввели число или число больше 60 или меньше минимального")

@router.message(Preferences.choose, F.text.casefold().in_(["да"]))
async def form_choose(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await app.database.requests.add_pref(message.from_user.id, data.get("gender"),
                                               int(data.get('age_min')), int(data.get("age_max")))
    await state.clear()
    await message.answer('Ваша анкета была сохранена', reply_markup=kb.greeting.as_markup(resize_keyboard=True))



@router.message(Preferences.choose, F.text.casefold().in_(["нет"]))
async def form_choose_no(message: types.Message, state: FSMContext):
    await message.answer("Тогда выберите то, что вам нужно.", reply_markup=kb.greeting.as_markup(resize_keyboard=True))
    await state.clear()
