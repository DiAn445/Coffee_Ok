from bot_creator import dp
from aiogram.utils import executor
import logging
from handlers import client, admin, other
from DataBase import sqlite_db

logging.basicConfig(level=logging.INFO)
sqlite_db.sql_start()

client.reg_handlers(dp)
admin.reg_handlers_admin(dp)
other.reg_handlers(dp)


executor.start_polling(dp, skip_updates=True)
