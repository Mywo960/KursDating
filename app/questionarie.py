from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import app.database.requests
import keyboard as kb
import aiosqlite
from app.states import *
import app.database.requests


router = Router()

@router.message(Command("Моя_анкета"))
async def my_ancete(message: types.Message, state: FSMContext):
   if await app.database.requests.is_user_registered(message.from_user.id):
       user_data = await app.database.requests.get_user_data(message.from_user.id)
       await message.answer("Ваша анкета")
       print(user_data)
       formatted_text = []
       photo_file_id = user_data[-1]
       formatted_text.append(f"Имя: {user_data[2]}\n"
                             f"Пол: {user_data[4]}\n"
                             f"Возраст: {user_data[5]}\n"
                             f"Город: {user_data[3]}\n"
                             f"О себе: {user_data[6]}\n"
                             )
       await message.answer_photo(
           photo_file_id,
           "\n".join(formatted_text), reply_markup=kb.my_ancete.as_markup(resize_keyboard=True, one_time_keyboard=True)
       )
   else:
       await message.answer("У вас пока что нет анкеты. Для начала введите своё имя")
       await state.set_state(Form.name)

@router.message(Command("Заполнить_заново"))
async def again_ancete(message: types.Message, state: FSMContext):
    await app.database.requests.del_user_data(message.from_user.id)
    await message.answer("Для начала введите имя.")
    await state.set_state(Form.name)

@router.message(Command("Удалить_анкету"))
async def del_ancete(message: types.Message, state: FSMContext):
    await app.database.requests.del_user_data(message.from_user.id)
    await state.clear()
    await message.answer("Ваша анкета была удалена", reply_markup=kb.greeting.as_markup(resize_keyboard=True))



@router.message(Command("Заполнить_профиль"))
async def fill_profile(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Давай начнём. Для начала введи своё имя")

@router.message(Form.name)
async def form_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer(f"Отлично, {message.text}, теперь введи свой возраст")

@router.message(Form.age)
async def form_gender(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 60:
        await state.update_data(age=message.text)
        await state.set_state(Form.gender)
        await message.answer(f"Тебе {message.text} лет. Теперь давай определимся с полом.",
                             reply_markup=kb.gender.as_markup(resize_keyboard=True, one_time_keyboard=True))
    else:
        await message.answer("Вы неправильно ввели число или вы слишком молоды/стары")

@router.message(Form.gender, F.text.casefold().in_(["парень", "девушка"]))
async def form_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Form.location)
    await message.answer("Укажите город вашего проживания")

@router.message(Form.gender)
async def form_gender_incorrect(message: types.Message, state: FSMContext):
    await message.answer("Нажмите на кнопку", reply_markup=kb.gender.as_markup(resize_keyboard=True, one_time_keyboard=True))


@router.message(Form.location)
async def form_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text.lower())
    await state.set_state(Form.about)
    await message.answer("Теперь расскажите о себе")

@router.message(Form.about)
async def form_about(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Расскажи побольше о себе")
    else:
        await state.update_data(about=message.text)
        await state.set_state(Form.photo)
        await message.answer("Теперь отправь своё фото")



@router.message(Form.photo, ~F.photo)
async def form_photo_incorrect(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото!")

@router.message(Form.photo, F.photo)
async def form_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    await state.set_state(Form.choose)

    formatted_text = []

    formatted_text.append(f"Имя: {data.get('name')}\n"
                          f"Пол: {data.get('gender')}\n"
                          f"Возраст: {data.get('age')}\n"
                          f"Город: {data.get('location')}\n"
                          f"О себе: {data.get('about')}\n"
                          )
    await message.answer_photo(
        photo_file_id,
        "\n".join(formatted_text)
    )
    await message.answer("Сохранить анкету?", reply_markup=kb.chooseb.as_markup(resize_keyboard=True, one_time_keyboard=True))






@router.message(Form.choose, F.text.casefold().in_(["да"]))
async def form_choose(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await app.database.requests.add_ancete(message.from_user.id, data.get('name'), data.get('location'),data.get("gender"),
                                               int(data.get('age')), data.get("about"), data.get("photo"))
    await state.clear()
    await message.answer('Ваша анкета была сохранена', reply_markup=kb.greeting.as_markup(resize_keyboard=True))



@router.message(Form.choose, F.text.casefold().in_(["нет"]))
async def form_choose_no(message: types.Message, state: FSMContext):
    await message.answer("Тогда выберите то, что вам нужно.", reply_markup=kb.greeting.as_markup(resize_keyboard=True))
    await state.clear()



@router.message()
async def error_text(message: types.Message):
    await message.answer("Я не знаю такой команды")