from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

upload_bt = KeyboardButton('/upload')
cancel_bt = KeyboardButton('/cancel')
start_bt = KeyboardButton('/start')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(upload_bt, cancel_bt).add(start_bt)
