import json
from datetime import datetime

from aiogram import types
from os.path import exists
from calendar_handler import FILE_NAME


# Функция для получения будущих записей
def get_future_appointments():
    now = datetime.now()
    if exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            appointments = json.load(f)

        # Преобразование записей в объекты datetime
        future_appointments = [
            appointment for appointment in appointments
            if datetime.strptime(appointment['datetime'], "%Y-%m-%d %H:%M") >= now
        ]

        # Сортировка по времени
        future_appointments.sort(key=lambda x: datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M"))

        return future_appointments

    return []

# Функция для вывода будущих записей
async def command_my_lessons(message: types.Message):
    user_id = message.from_user.id
    appointments = get_user_appointments(user_id)
    future_appointments = get_future_appointments()

    if future_appointments:
        response = "Ваши записи на будущие уроки:\n\n"
        for appointment in future_appointments:
            response += f"- {appointment['datetime']}\n"
        await message.answer(response)
    else:
        await message.answer("У вас нет будущих записей на уроки.")

# Функция для получения записей пользователя
def get_user_appointments(user_id):
    appointments = get_future_appointments()
    return [appointment for appointment in appointments if appointment['user_id'] == user_id]
