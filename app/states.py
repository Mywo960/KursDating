from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    choose = State()
    name = State()
    gender = State()
    age = State()
    location = State()
    about = State()
    photo = State()

class Preferences(StatesGroup):
    gender = State()
    age_min = State()
    age_max = State()
    choose = State()

class Finding(StatesGroup):
    stat = State()
    finding = State()


class Answer(StatesGroup):
    stat = State()
    answer = State()

