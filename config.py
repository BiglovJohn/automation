import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

"""
Файл с ключами

KEY (str): Токен для Telegram API
bot (class): Инициализация бота с помощью токена SECRET_TOKEN
"""

load_dotenv()

storage = MemoryStorage()
bot = Bot(os.getenv('KEY'))
dp = Dispatcher(bot, storage=storage)


class BusinessTripForm(StatesGroup):
    """State для поэтапного получения данных от пользователя"""

    city = State()  # Будет представлен в storage как 'Form:name'
    first_date = State()
    last_date = State()
    transfer_expenses = State()
    representative_expenses = State()


class BusinessTripEditForm(StatesGroup):
    """State для поэтапного получения данных от пользователя"""

    city = State()  # Будет представлен в storage как 'Form:name'
    first_date = State()
    last_date = State()
    transfer_expenses = State()
    representative_expenses = State()
