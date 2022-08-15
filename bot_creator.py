from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='5539927184:AAHgUjfxubZBti0RhHG4k6rMbD1aCUuUTLM', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
