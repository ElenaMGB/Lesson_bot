import logging
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
import locale
import json
from os.path import exists


# Устанавливаем русскую локаль
locale.setlocale(locale.LC_TIME, 'ru_RU')

# Файл для хранения записей
FILE_NAME = 'appointments.json'

class CustomCalendar(CallbackData, prefix="calendar"):
    action: str
    date: str

class AppointmentStates(StatesGroup):
    waiting_for_time = State()
    # waiting_for_date = State()

def create_calendar(start_date: datetime = datetime.now()):
    keyboard = []
    row = []

    # Получаем день недели для первой даты календаря (0 - Пн, 6 - Вс)
    start_day_of_week = start_date.weekday()
    
    # Создаем список дней недели, начиная с нужного дня недели
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    adjusted_days_of_week = days_of_week[start_day_of_week:] + days_of_week[:start_day_of_week]

    # Первая строка - дни недели
    row = [InlineKeyboardButton(text=day, callback_data="ignore") for day in adjusted_days_of_week]
    keyboard.append(row)

    row = []
    for i in range(21):  # 14 дней = 2 недели
        date = start_date + timedelta(days=i)
        button_text = date.strftime("%d (%a)")  # Форматируем кнопку как "число (день недели)"
        button = InlineKeyboardButton(
            text=date.strftime("%d"),
            callback_data=CustomCalendar(action="day", date=date.strftime("%Y-%m-%d")).pack()
        )
        row.append(button)
        if len(row) == 7 or i == 20:
            keyboard.append(row)
            row = []
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def command_calendar(message: types.Message):
    await message.answer("Пожалуйста, выберите дату:", reply_markup=create_calendar())

async def process_calendar_selection(callback_query: types.CallbackQuery, callback_data: CustomCalendar, state: FSMContext):
    selected_date = datetime.strptime(callback_data.date, "%Y-%m-%d")
    await state.update_data(selected_date=selected_date)
    logging.info(f"Сохранена дата: {selected_date}")
    await state.set_state(AppointmentStates.waiting_for_time)
    await callback_query.message.answer(f"Вы выбрали дату: {selected_date.strftime('%d.%m.%Y')}")
    await callback_query.message.answer("Теперь введите время в формате ЧЧ:ММ")


def create_confirmation_keyboard():
    keyboard =InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="confirm_yes"),
            InlineKeyboardButton(text="Нет, вернуться к выбору даты", callback_data="confirm_no")
        ],
        [InlineKeyboardButton(text="Выйти", callback_data="exit")]
    ])
    return keyboard

async def exit_appointment(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Вы вышли из процесса записи. Если хотите записаться снова, используйте команду /calendar.")
    await callback_query.answer()

# async def process_time_input(message: types.Message, state: FSMContext):
#     logging.info(f"Получено время: {message.text}")
#     try:
#         time = datetime.strptime(message.text, "%H:%M").time()
#         # Сохраняем выбранное время в состоянии
#         await state.update_data(selected_time=time)
#         # Получаем дату из состояния (предполагается, что вы сохранили её там ранее)
#         data = await state.get_data()
#         selected_date = data.get('selected_date')
#         logging.info(f"Сохраненные данные: date={selected_date}, time={time}")
#         if selected_date:
#             # Получаем день недели на русском (например, "пятница")
#             day_of_week = selected_date.strftime("%A")
#             # Комбинируем дату и время
#             full_datetime = datetime.combine(selected_date, time)
#                         # Формируем сообщение с датой, временем и днем недели
#             await message.answer(
#                 f"Вы выбрали дату и время: {full_datetime.strftime('%d.%m.%Y %H:%M')} ({day_of_week})"
#             )
#             # Отправляем сообщение с кнопками "Да" и "Нет"
#             await message.answer("Записаться?", reply_markup=create_confirmation_keyboard())
#         else:
#             await message.answer("Произошла ошибка. Пожалуйста, начните процесс выбора даты заново.")
#         # await state.clear() #очистка состояния
#     except ValueError:
#         await message.answer("Пожалуйста, введите время в формате ЧЧ:ММ")

# @dp.message_handler(state=AppointmentStates.waiting_for_time)
async def process_time_input(message: types.Message, state: FSMContext):
    logging.info(f"Получено время: {message.text}")
    try:
        time = datetime.strptime(message.text, "%H:%M").time()
        # Сохраняем выбранное время в состоянии
        await state.update_data(selected_time=time)
         # Получаем дату из состояния (предполагается, что вы сохранили её там ранее)
        data = await state.get_data()
        # logging.info(f"Сохраненные данные после ввода времени: {data}")
        selected_date = data.get('selected_date')
        logging.info(f"Сохраненные данные: date={selected_date}, time={time}")

        if selected_date:
            # Получаем день недели на русском (например, "пятница")
            day_of_week = selected_date.strftime("%A")
            # Комбинируем дату и время
            full_datetime = datetime.combine(selected_date, time)
            
            # Формируем и отправляем сообщение с подтверждением
            # await message.answer(f"Вы выбрали: {selected_date.strftime('%d.%m.%Y')} в {time.strftime('%H:%M')}. Это {day_of_week}.")
            await message.answer(
                f"Вы выбрали дату и время: {full_datetime.strftime('%d.%m.%Y %H:%M')} ({day_of_week})"
            )
                # Отправляем сообщение с кнопками "Да" и "Нет"
            await message.answer(
                "Записаться?", reply_markup=create_confirmation_keyboard()
            )
        else:
            await message.answer("Дата не выбрана. Пожалуйста, выберите сначала дату.")
    
    except ValueError:
        await message.answer("Ошибка: Введите время в формате ЧЧ:ММ, например, 14:30.")

async def confirm_yes(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info("Обработчик confirm_yes вызван")  # Логирование для отладки

    data = await state.get_data()
    logging.info(f"Данные из состояния: {data}")

    selected_date = data.get('selected_date')
    selected_time = data.get('selected_time')

    if selected_date and selected_time:
        # Логирование выбранной даты и времени
        logging.info(f"Выбрана дата: {selected_date}, время: {selected_time}")

        user_id = callback_query.from_user.id
        full_datetime = datetime.combine(selected_date, selected_time)
        record = {"user_id": user_id, "datetime": full_datetime.strftime("%Y-%m-%d %H:%M")}

        # Логирование записи перед сохранением в файл
        logging.info(f"Записываем данные: {record}")

        # Чтение существующих записей
        appointments = []
        if exists(FILE_NAME):
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                appointments = json.load(f)

        # Добавляем новую запись
        appointments.append(record)

        # Сохраняем обновленные записи в файл
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(appointments, f, ensure_ascii=False, indent=4)

        # Подсчитываем количество записей для данного пользователя
        count = sum(1 for appointment in appointments if appointment['user_id'] == user_id)

        # Сообщаем пользователю об успешной записи
        await callback_query.message.answer(f"Успешно! Всего записаны на {count} занятий.")
        # await callback_query.message.answer(f"Успешно! Всего записаны на {count} занятий.", reply_markup=create_start_keyboard())
    else:
        logging.error("Не найдены дата или время")

    await callback_query.answer()

async def confirm_no(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать новую дату", callback_data="new_date")], #или new_date_selection?
        [InlineKeyboardButton(text="Выйти", callback_data="exit")]
    ])
    await callback_query.message.answer("Что вы хотите сделать?", reply_markup=keyboard)
    await callback_query.answer()

async def new_date_selection(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Пожалуйста, выберите новую дату:", reply_markup=create_calendar())
    await callback_query.answer()

# async def command_my_lessons(message: types.Message):
#     user_id = message.from_user.id
#     appointments = get_user_appointments(user_id)
#     if appointments:
#         response = "Ваши записи на уроки:\n\n"
#         for appointment in appointments:
#             response += f"- {appointment['datetime']}\n"
#         await message.answer(response)
#     else:
#         await message.answer("У вас пока нет записей на уроки.")

# def get_user_appointments(user_id):
#     if exists(FILE_NAME):
#         with open(FILE_NAME, 'r', encoding='utf-8') as f:
#             appointments = json.load(f)
#         return [appointment for appointment in appointments if appointment['user_id'] == user_id]
#     return []

def setup_calendar_handlers(dp: Dispatcher):
    dp.message.register(command_calendar, Command("calendar"))
    dp.callback_query.register(process_calendar_selection, CustomCalendar.filter())
    dp.message.register(process_time_input, StateFilter(AppointmentStates.waiting_for_time))
    dp.callback_query.register(confirm_yes,
                               lambda callback: callback.data == "confirm_yes", 
                               StateFilter("*"))
    dp.callback_query.register(confirm_no, lambda callback: callback.data == "confirm_no")
    dp.callback_query.register(exit_appointment, lambda callback: callback.data == "exit")
    dp.callback_query.register(new_date_selection, lambda callback: callback.data == "new_date")
