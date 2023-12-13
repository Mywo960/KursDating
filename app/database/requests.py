import aiosqlite
from aiogram import types

# Функция для добавления других данных в базу данных
async def add_ancete(user_id: int, name: str, location: str,  gender: str, age: int, about: str, photo: str):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        update_query = f"INSERT INTO users (tgid, name, location ,gender, age, about, photo) VALUES ({user_id}," \
                       f" '{name}' , '{location}' ,'{gender}', {age}, '{about}', '{photo}');"
        await cursor.execute(update_query)
        await db.commit()

async def add_pref(user_id: int, gender: str, age_min: int, age_max: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        update_query = f"INSERT INTO preferences (tgid, gender, age_min, age_max) VALUES ({user_id}, '{gender}', {age_min}, {age_max});"
        await cursor.execute(update_query)
        await db.commit()

# Функция для проверки регистрации пользователя
async def is_user_registered(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT 1 FROM users WHERE tgid = ?", (str(user_id),))
        return bool(await cursor.fetchone())

async def get_user_data(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM users WHERE tgid = ?", (str(user_id),))
        user_data = await cursor.fetchone()
    return user_data

async def get_pref_data(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM preferences WHERE tgid = ?", (str(user_id),))
        user_data = await cursor.fetchone()
    return user_data

async def del_user_data(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("DELETE FROM users WHERE tgid = ?", (str(user_id),))
        await db.commit()

async def del_pref_data(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("DELETE FROM preferences WHERE tgid = ?", (str(user_id),))
        await db.commit()

async def is_pref_registered(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT 1 FROM preferences WHERE tgid = ?", (str(user_id),))
        return bool(await cursor.fetchone())


async def get_users_data_except_me(tgid: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT location FROM users WHERE tgid = ?", (str(tgid),))
        location = await cursor.fetchone()

        await cursor.execute("SELECT * FROM preferences WHERE tgid = ?", (str(tgid),))
        pref = await cursor.fetchone()

        await cursor.execute(
            f"SELECT * FROM users WHERE age > ? AND age < ? AND gender = ? AND tgid <> ? AND location <> ?",
            (str(pref[3]), str(pref[4]), str(pref[2]), str(tgid), str(location)))
        user_data = await cursor.fetchall()
    return user_data

async def set_matches_like(user1_id: int, user2_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        update_query = f"INSERT INTO matches (tgid1, type1, tgid2 ) VALUES ({user1_id}, 'like' , {user2_id});"
        await cursor.execute(update_query)
        await db.commit()


async def look_like(user_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute(
            f"SELECT tgid1 FROM matches WHERE tgid2 = ?", (str(user_id),))
        user_data = await cursor.fetchall()
    return user_data

async def get_users_data(users_id: int):
    async with aiosqlite.connect('app/database/dating_bot.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM users WHERE tgid = ?", str(users_id))
        users_data = await cursor.fetchone()
    return users_data

