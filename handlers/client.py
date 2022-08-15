from aiogram import types, Dispatcher
from bot_creator import bot, dp
from Keyboards.client_kb import client_keyboard
from DataBase import sqlite_db


async def command_start(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, 'Greetings!', reply_markup=client_keyboard)
        await answer.delete()
    except:
        await answer.reply(
            """<b><i>U can communicate with bot only in private messages
            Please, text him</i></b>\n
            <b>https://t.me/Coffe_Ok_bot</b>
            """)


async def command_contacts(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, '<b>Kiev, golden gates 15\n10:00 - 20:00</b>')
        await answer.delete()
    except:
        await answer.reply(
            """<b><i>U can communicate with bot only in private messages
            Please, text him</i></b>\n
            <b>https://t.me/Coffe_Ok_bot</b>
            """)


async def command_order(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, 'Ordering!')
        await answer.delete()
        await sqlite_db.sql_read(answer)
    except:
        await answer.reply(
            """<b><i>U can communicate with bot only in private messages
            Please, text him</i></b>\n
            <b>https://t.me/Coffe_Ok_bot</b>
            """)

async def get_basket(answer: types.Message):
    try:
        await sqlite_db.sql_ordering(answer.from_user.id)
        await bot.send_message(answer.from_user.id, '🧺 Your basket:')
        await answer.delete()
        await sqlite_db.show_my_order(answer)
    except:
        await answer.reply(
            """<b><i>U can communicate with bot only in private messages
            Please, text him</i></b>\n
            <b>https://t.me/Coffe_Ok_bot</b>
            """)


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_contacts, commands=['contacts'])
    dp.register_message_handler(command_order, commands=['order'])
    dp.register_message_handler(get_basket, commands=['basket'])