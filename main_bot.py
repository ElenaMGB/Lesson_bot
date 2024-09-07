import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

from future_appointments import command_my_lessons

import config
import random_fox
import weather
from calendar_handler import setup_calendar_handlers, command_calendar

# Инициализация
API_TOKEN = config.token_api
weather_api_key = config.weather_api_key
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Клавиатура для стартового меню
def create_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Лиса"), KeyboardButton(text="Погода")],
            [KeyboardButton(text="Запись"), KeyboardButton(text="Мои уроки")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def command_start(message: types.Message):
    name = message.chat.first_name
    await message.answer(f"Привет, {name}! Я бот на aiogram 3.\nИспользуй /help для получения списка команд.\nВыберите действие:", reply_markup=create_start_keyboard())

@dp.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer("Команды:\n/fox - получить картинку лисы\n/погода - информация о погоде\n/calendar - для записи на урок")

@dp.message(Command("fox"))
async def command_fox(message: types.Message):
    await message.answer(f"Вот ссылка на картинку лисы: {random_fox.fox()}")

@dp.message(Command("погода"))
async def command_weather(message: types.Message):
    city = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else "Yekaterinburg"
    weather_info = weather.get_weather_info(city)
    await message.reply(weather_info)

@dp.message(lambda message: message.text == "Лиса")
async def button_fox(message: types.Message):
    await command_fox(message)

@dp.message(lambda message: message.text == "Погода")
async def button_weather(message: types.Message):
    await command_weather(message)

@dp.message(lambda message: message.text == "Запись")
async def button_appointment(message: types.Message):
    await command_calendar(message)

@dp.message(lambda message: message.text == "Мои уроки")
async def button_my_lessons(message: types.Message):
    await command_my_lessons(message)

@dp.message(lambda message: message.text == "Повтори")
async def echo(message: types.Message):
    await message.answer(message.text)

# Настройка обработчиков
# setup_calendar_handlers(dp)

# Запуск бота
async def main():
    setup_calendar_handlers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
