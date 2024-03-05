# Админка
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext

import database
import texts.admin
from config import admins_list
from database import *
from keyboards import *


# Добавляем новую команду /admin
async def admin_entry(message: types.Message):
    # Проверяем есть ли айди пользователя в списке admins
    if message.from_user.id in admins_list:
        # Если есть, то открываем панель
        await message.answer("Вы открыли панель администратора",
                             parse_mode="HTML", reply_markup=admin_panel_kb)
    else:
        # Если нет, то говорим об этом
        await message.answer("Вы не администратор", parse_mode="HTML",
                             reply_markup=None)


# Обработка кнопки "👨‍👩‍👦‍👦 Пользователи"
async def call_users(call: types.CallbackQuery):
    # Вызываем написанную ранее функцию, которая возвращает строку с выводом пользователей бота
    await call.message.answer(show_users(), reply_markup=back_to_admin_kb)
    await call.answer()


# Обработка кнопки "📊 Статистика"
async def call_statistics(call: types.CallbackQuery):
    # Вызываем написанную ранее функцию, которая возвращает количество пользователей
    await call.message.answer(f"Количество пользователей: {show_statistics()}",
                              reply_markup=back_to_admin_kb)
    await call.answer()


# Создадим машину состояний для блокировки по id
class AdminState(StatesGroup):
    BAN = State()
    UNBAN = State()
    ADD_HOUSE = State()
    mailing_step1 = State()
    mailing_step2 = State()


# Обработчик кнопки "⛔️ Блокировка"
async def call_ban_user(call: types.CallbackQuery):
    # Просим ввести id пользователя для блокировки
    await call.message.answer(texts.admin.ban_from_admin_start,
                              parse_mode="HTML",
                              reply_markup=types.ReplyKeyboardRemove())
    # Запоминаем ответ пользователя
    await call.answer()
    await AdminState.BAN.set()


# Обработчик введённого администратором id для блокирвоки
async def add_to_ban(message: types.Message, state: FSMContext):
    from main import bot

    text = message.text

    if text == '/cancel':
        await message.answer(texts.admin.ban_from_admin_cancel,
                             reply_markup=admin_panel_kb)
        await state.finish()
        return

    if text.isdigit():
        id_to_ban = int(text)
        try:
            await bot.send_message(id_to_ban, texts.admin.ban)
        except Exception as e:
            print(e)
        database.add_user_to_block(id_to_ban)
        await message.answer(texts.admin.ban_from_admin_finaly,
                             parse_mode='HTML', reply_markup=admin_panel_kb)
        await state.reset_state()
    else:
        await message.answer(texts.admin.ban_from_admin_except,
                             parse_mode='HTML')


async def call_back_admin(call: types.CallbackQuery):
    await call.message.edit_text(texts.admin.start, parse_mode="HTML",
                                 reply_markup=admin_panel_kb)
    await call.answer()


# Обработчик кнопки "✅ Разблокировка"
async def call_unlock_user(call: types.CallbackQuery):
    # Просим ввести id пользователя для блокировки
    await call.message.answer(texts.admin.unban_from_admin_start,
                              parse_mode="HTML",
                              reply_markup=types.ReplyKeyboardRemove())
    # Запоминаем ответ пользователя
    await call.answer()
    await AdminState.UNBAN.set()


# Обработчик введённого администратором id для разблокировки
async def unban(message: types.Message, state: FSMContext):
    from main import bot

    text = message.text
    if text == '/cancel':
        await message.answer(texts.admin.unban_from_admin_cancel,
                             reply_markup=admin_panel_kb)
        await state.finish()
        return

    if text.isdigit():
        id_to_unban = int(text)
        try:
            await bot.send_message(id_to_unban, texts.admin.unban)
        except Exception as e:
            print(e)
        database.unlock_users(id_to_unban)
        await message.answer(texts.admin.unban_from_admin_finaly,
                             parse_mode='HTML', reply_markup=admin_panel_kb)
        await state.finish()
    else:
        await message.answer(texts.admin.ban_from_admin_except,
                             parse_mode='HTML')


async def call_add_house_callback(callback_query: types.CallbackQuery):
    # Просим ввести улицу и номер дома
    await callback_query.message.answer("Введите улицу и номер дома в "
                                        "формате 'Улица, Номер дома':",
                                        reply_markup=types.ReplyKeyboardRemove())
    await AdminState.ADD_HOUSE.set()


# Обработчик введенной информации для добавления дома
async def process_add_house(message: types.Message, state: FSMContext):
    # Получаем введенную информацию
    input_data = message.text

    # Разделяем улицу и номер дома по запятой
    data_parts = input_data.split(',')

    # Проверяем, что введены оба значения
    if len(data_parts) != 2:
        await message.answer("Некорректный формат. Введите улицу и номер "
                             "дома в формате 'Улица, Номер дома'.", )
        return

    # Удаляем лишние пробелы
    street = data_parts[0].strip()
    house_number = data_parts[1].strip()

    # Добавляем новый дом в базу данных
    database.add_house(street, house_number)

    # Отправляем сообщение об успешном добавлении
    await message.answer(f"Дом '{street}, {house_number}' успешно добавлен.",
                         reply_markup=admin_panel_kb)

    # Сбрасываем состояние
    await state.finish()


async def mailing(call: types.CallbackQuery):
    instructions = "Введите текст сообщения:"
    await call.message.answer(instructions,
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()
    await AdminState.mailing_step1.set()


async def mailing1(message, state):
    await state.update_data(text=message.text)

    instructions = "Прикрепите фотографию к сообщению:"
    await message.answer(text=instructions)

    await AdminState.mailing_step2.set()


async def mailing2(message, state):
    from main import bot

    await message.photo[-1].download(destination_file='files/photo.jpg')
    data = await state.get_data()
    subscribers = database.users_id()

    c = 0
    for (user_id,) in subscribers:
        try:
            with open('files/photo.jpg', 'rb') as f:
                await bot.send_photo(user_id, f, data['text'])
            c += 1
        except Exception as e:
            print(e)

    await message.answer(
        f'Рассылка успешно завершена: {c} / {database.show_statistics()}',
        reply_markup=admin_panel_kb)
    await state.finish()
