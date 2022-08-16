from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
