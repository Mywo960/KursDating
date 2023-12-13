from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


greeting = ReplyKeyboardBuilder()
greeting.button(text=f"/Просмотр_анкет")
greeting.button(text=f"/Моя_анкета")
greeting.button(text=f"/Предпочтения")
greeting.adjust(1)


my_pref = ReplyKeyboardBuilder()
my_pref.button(text='/Заполнить_предпочтения_заново')
my_pref.button(text='/Удалить_предпочтения')
my_pref.adjust(1)

my_ancete = ReplyKeyboardBuilder()
my_ancete.button(text='/Заполнить_заново')
my_ancete.button(text='/Удалить_анкету')

gender = ReplyKeyboardBuilder()
gender.button(text=f"Парень")
gender.button(text=f"Девушка")

chooseb = ReplyKeyboardBuilder()
chooseb.button(text=f"Да")
chooseb.button(text=f"Нет")

is_like = ReplyKeyboardBuilder()
is_like.button(text=f"❤️")
is_like.button(text=f"👎")

get_like = ReplyKeyboardBuilder()
get_like.button(text=f"/Посмотреть")