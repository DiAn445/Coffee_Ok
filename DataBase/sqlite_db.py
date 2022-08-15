import sqlite3
from bot_creator import bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


def sql_start():
    global base, cursor
    base = sqlite3.connect('Coffee_base.db')
    cursor = base.cursor()
    if base:
        print('Data base connected!')
        base.execute(
            "CREATE TABLE IF NOT EXISTS articles(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
        base.commit()


async def sql_add_commands(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO articles VALUES (?,?,?,?)", tuple(data.values()))
        base.commit()


async def sql_read(answer: Message):
    for i in cursor.execute("SELECT * FROM articles").fetchall():
        await bot.send_photo(answer.from_user.id, i[0], f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]}',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton(text='🧺 order', callback_data=f"done {i[1]}, {i[2]}, {i[3]}")))


async def sql_read_as_list():
    return cursor.execute('SELECT * FROM articles').fetchall()


async def sql_deleter(item):
    cursor.execute('DELETE FROM articles WHERE name == ?', (item,))
    base.commit()


async def sql_ordering(user_id):
    base.execute(
        f"CREATE TABLE IF NOT EXISTS user_{user_id}(name TEXT, description TEXT, price TEXT)")
    base.commit()


async def add_order(user_id, name, description, price):
    cursor.execute(f"INSERT INTO user_{user_id} VALUES (?,?,?)", (name, description, price))
    base.commit()


async def show_my_order(answer: Message):
    gen = cursor.execute(f"SELECT * FROM user_{answer.from_user.id}").fetchall()
    basket = ""
    sum_of_order = [float(i[2]) for i in gen]
    if len(gen) == 0:
        await bot.send_message(answer.from_user.id, 'Basket is empty!')
        return
    for i in gen:
        basket += f'Name: {i[0]} Description: {i[1]}\nPrice: {i[2]}\n'
    await bot.send_message(answer.from_user.id, basket + f"\nTotal price: {sum(sum_of_order)}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton(text='clean basket', callback_data='clean_basket ')))


