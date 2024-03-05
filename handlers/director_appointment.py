import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
import gspread
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
from keyboards import *

# Подключение к Google Sheets
gc = gspread.service_account(filename=config.google_sheets_file_key)
# Открываем google нашу таблицу
sh = gc.open("Запись к директору")
# выбираем лист
worksheet = sh.sheet1


class DirectorAppointmentStates(StatesGroup):
    QUESTION = State()
    APPOINTMENT_TIME = State()


async def handle_director_appointment(message: aiogram.types.Message):
    # сначала проверяем наличие свободного времени на четверг
    await message.answer("Секунду, я уточняю расписание директора на "
                         "ближайший четверг...")
    next_thursday = get_next_thursday()

    # Ищем ячейку с ближайшим четвергом
    date_range = worksheet.range(config.DATE_RANGE)
    thursday_cell = find_thursday_cell(date_range, next_thursday)

    # Ищем свободные ячейки в диапазоне времени
    time_range = worksheet.range(config.TIME_RANGE)
    available_times = []
    for i, time_cell in enumerate(time_range):
        date_cell = worksheet.cell(thursday_cell.row, time_cell.col)
        if date_cell.value is None:
            available_times.append(time_range[i].value)

    if not available_times:
        next_friday = next_thursday + timedelta(days=1)
        await message.answer(
            f"Все время на ближайший четверг "
            f"{next_thursday.strftime('%d.%m.%Y')} занято. "
            f"Следующая запись на четверг будет доступна в пятницу "
            f"({next_friday.strftime('%d.%m.%Y')}).")
        return

    # Запрашиваем вопрос пользователя
    await message.answer(
        "Введите вопрос, о котором вы хотите поговорить с директором:",
        reply_markup=ReplyKeyboardRemove())
    await DirectorAppointmentStates.QUESTION.set()


async def handle_question(message: aiogram.types.Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)

    await message.answer("Секунду, я уточняю расписание директора...")

    # Запрашиваем время начала встречи
    await message.answer("Выберите время начала встречи:",
                         reply_markup=get_time_keyboard())
    await DirectorAppointmentStates.APPOINTMENT_TIME.set()


async def handle_appointment_time(callback_query: aiogram.types.CallbackQuery,
                                  state: FSMContext):
    appointment_time = callback_query.data
    if appointment_time == "back":
        await callback_query.message.answer("Вы отменили запись к "
                                            "директору", reply_markup=start_kb)
        await state.finish()
        return

    data = await state.get_data()
    question = data.get('question')

    # Получаем ближайший четверг
    next_thursday = get_next_thursday()

    # Ищем ячейку с ближайшим четвергом
    date_range = worksheet.range(config.DATE_RANGE)
    thursday_cell = find_thursday_cell(date_range, next_thursday)

    if thursday_cell is None:
        await callback_query.message.answer(
            "Выбранное время недоступно. Пожалуйста, выберите другое время.")
        return

    # Ищем ячейку с выбранным временем
    time_range = worksheet.range(config.TIME_RANGE)
    time_cell = None
    for cell in time_range:
        if cell.value == appointment_time:
            time_cell = cell
            break

    if time_cell is None:
        await callback_query.message.answer(
            "Выбранное время недоступно. Пожалуйста, выберите другое время.")
        return

    # Записываем вопрос в ячейку
    question_cell = worksheet.cell(thursday_cell.row, time_cell.col)
    if question_cell.value is None:
        worksheet.update_cell(thursday_cell.row, time_cell.col, question)
        # worksheet.update(time_cell.address, 'занято')
        await callback_query.message.answer(
            f"Вы успешно записаны на {next_thursday.strftime('%d.%m.%Y')} в "
            f"{appointment_time} по вопросу {question}", reply_markup=start_kb)
        await state.finish()
    else:
        await callback_query.message.answer(
            "Выбранное время уже занято. Пожалуйста, выберите другое время.")


def get_time_keyboard():
    # Ищем ближайший четверг
    next_thursday = get_next_thursday()

    # Ищем ячейку с ближайшим четвергом
    date_range = worksheet.range(config.DATE_RANGE)
    thursday_cell = find_thursday_cell(date_range, next_thursday)

    # Ищем свободные ячейки в диапазоне времени
    time_range = worksheet.range(config.TIME_RANGE)
    available_times = []
    for i, time_cell in enumerate(time_range):
        date_cell = worksheet.cell(thursday_cell.row, time_cell.col)
        if date_cell.value == None:
            available_times.append(time_range[i].value)

    # Создаем клавиатуру с доступным временем
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=time, callback_data=time) for time in
               available_times]
    keyboard.add(*buttons)  # Добавляем кнопки в клавиатуру

    # Добавляем кнопку "Назад" в клавиатуру
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="back"))

    return keyboard


def get_next_thursday():
    today = datetime.today()
    days_ahead = (3 - today.weekday()) % 7
    next_thursday = today + timedelta(days=days_ahead)

    # Если сегодня четверг, то предлагаем время следующего четверга
    if today.weekday() == 3:
        next_thursday += timedelta(days=7)

    return next_thursday


def find_thursday_cell(date_range, next_thursday):
    for cell in date_range:
        if cell.value == next_thursday.strftime('%d.%m.%Y'):
            return cell
    return None
