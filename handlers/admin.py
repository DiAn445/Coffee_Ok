from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot_creator import bot, dp
from aiogram.dispatcher.filters import Text
from DataBase import sqlite_db
from Keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def if_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'ready to work!', reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def cancel_state(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('canceled')


async def uploader(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('upload photo:')


async def upload_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('input name:')


async def input_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == '/cancel':
            await cancel_state(message, state)
            return
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('input description:')


async def input_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == '/cancel':
            await cancel_state(message, state)
            return
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('input price:')


async def input_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == '/cancel':
            await cancel_state(message, state)
            return
        async with state.proxy() as data:
            data['price'] = float(message.text)
        async with state.proxy() as data:
            await message.reply(str(data))
        await sqlite_db.sql_add_commands(state)
        await state.finish()


async def del_callback_command(callback_query: types.CallbackQuery):
    await sqlite_db.sql_deleter(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} deleted!", show_alert=True)


async def delete_item(item: types.Message):
    if item.from_user.id == ID:
        read = await sqlite_db.sql_read_as_list()
        for i in read:
            await bot.send_photo(item.from_user.id, i[0], f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]}',
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(text=f"Delete: {i[1]}", callback_data=f"del {i[1]}")))
        await item.delete()


async def done_callback_command(callback_query: types.CallbackQuery):
    res = [i for i in callback_query.data.replace('done ', '').split(',')]
    await sqlite_db.sql_ordering(str(callback_query.from_user.id))
    await sqlite_db.add_order(str(callback_query.from_user.id), *res)
    await callback_query.answer(text='order saved!', show_alert=True)


async def clean_basket(callback: types.CallbackQuery):
    sqlite_db.cursor.execute(f"DROP TABLE user_{callback.from_user.id}")
    sqlite_db.base.commit()
    await callback.answer(text='cleaned!', show_alert=True)

def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(uploader, commands=['upload'], state=None)
    dp.register_message_handler(upload_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(input_name, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(input_description, content_types=['text'], state=FSMAdmin.description)
    dp.register_message_handler(input_price, content_types=['text'], state=FSMAdmin.price)
    dp.register_message_handler(cancel_state, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(if_admin, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['delete'], is_chat_admin=True, state=None)
    dp.register_callback_query_handler(del_callback_command, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(done_callback_command, lambda x: x.data and x.data.startswith('done '))
    dp.register_callback_query_handler(clean_basket, lambda x: x.data and x.data.startswith('clean_basket '))