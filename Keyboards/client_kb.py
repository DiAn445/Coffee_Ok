from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#-----main menu

start_bt = KeyboardButton('/start')
contacts_bt = KeyboardButton('/contacts')
order_bt = KeyboardButton('/order')
get_ph_num_bt = KeyboardButton('☎️ leave your number', request_contact=True)
get_basket = KeyboardButton('/basket')

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
client_keyboard.row(start_bt, contacts_bt, order_bt).add(get_ph_num_bt, get_basket)





