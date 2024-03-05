from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)

import database
from keyboards import *
from config import ADMIN_CHAT_ID


##### Обработка заявки на сантехника ########################

# Машина состояний для заявки на сантехника
class PlumberState(StatesGroup):
    specialist = State()
    street = State()
    house = State()
    flat = State()
    problem = State()


# Функция для обработки кнопки "📨 Отправить заявку"
async def call_bid_plumber(callback_query: types.CallbackQuery, state: FSMContext):

    specialist = 'сантехника'
    await state.update_data(specialist=specialist)

    # Задаем вопрос пользователю и формируем список кнопок с названиями улиц
    question_text = "Выберите улицу, куда вы хотите вызвать сантехника:"
    # Функция для получения списка кнопок с названиями улиц
    streets = database.get_streets()

    # Создаем клавиатуру с улицами
    street_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=street, callback_data=street) for
               street in streets]
    street_keyboard.add(*buttons)  # Добавляем кнопки в клавиатуру

    # Обновляем состояние пользователя в PlumberState
    await callback_query.message.answer(text=question_text,
                                        reply_markup=street_keyboard)

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.street.set()

async def call_bid_electrician(callback_query: types.CallbackQuery, state: FSMContext):

    specialist = 'электрика'
    await state.update_data(specialist=specialist)

    # Задаем вопрос пользователю и формируем список кнопок с названиями улиц
    question_text = "Выберите улицу, куда вы хотите вызвать электрика':"
    # Функция для получения списка кнопок с названиями улиц
    streets = database.get_streets()

    # Создаем клавиатуру с улицами
    street_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=street, callback_data=street) for
               street in streets]
    street_keyboard.add(*buttons)  # Добавляем кнопки в клавиатуру

    # Обновляем состояние пользователя в PlumberState
    await callback_query.message.answer(text=question_text,
                                        reply_markup=street_keyboard)

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.street.set()



async def call_bid_other(callback_query: types.CallbackQuery, state:
FSMContext):

    specialist = 'специалиста'
    await state.update_data(specialist=specialist)

    # Задаем вопрос пользователю и формируем список кнопок с названиями улиц
    question_text = "Выберите улицу, куда вы хотите вызвать электрика':"
    # Функция для получения списка кнопок с названиями улиц
    streets = database.get_streets()

    # Создаем клавиатуру с улицами
    street_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=street, callback_data=street) for
               street in streets]
    street_keyboard.add(*buttons)  # Добавляем кнопки в клавиатуру

    # Обновляем состояние пользователя в PlumberState
    await callback_query.message.answer(text=question_text,
                                        reply_markup=street_keyboard)

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.street.set()


# Функция для обработки выбора улицы
async def call_street_selected(callback_query: types.CallbackQuery,
                               state: FSMContext):
    # Получаем данные о выбранной улице
    street = callback_query.data
    await state.update_data(street=street)

    # Задаем вопрос пользователю и формируем список кнопок с номерами домов
    question_text = "Выберите номер дома:"
    # Функция для получения списка кнопок с номерами домов по выбранной улице
    houses = database.get_houses_for_steet(street)

    # Создаем клавиатуру с номерами домов по улице
    houses_keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=house, callback_data=house) for
               house in houses]
    houses_keyboard.add(*buttons)  # Добавляем кнопки в клавиатуру

    # Отправляем вопрос пользователю с кнопками
    await callback_query.message.answer(text=question_text,
                                        reply_markup=houses_keyboard)

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.house.set()


# Функция для обработки выбора номера дома
async def call_house_selected(callback_query: types.CallbackQuery, state: FSMContext):
    house = callback_query.data
    await state.update_data(house=house)

    # Задаем вопрос пользователю и запрашиваем номер квартиры
    question_text = "Введите номер квартиры:"
    await callback_query.message.answer(text=question_text,
                         reply_markup=ReplyKeyboardRemove())

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.flat.set()


# Функция для обработки ввода номера квартиры
async def flat_input_handler(message: types.Message, state: FSMContext):
    flat = message.text
    await state.update_data(flat=flat)

    # Задаем вопрос пользователю и запрашиваем описание проблемы
    question_text = "Опишите вашу проблему:"
    await message.answer(text=question_text,
                         reply_markup=ReplyKeyboardRemove())

    # Обновляем состояние пользователя в PlumberState
    await PlumberState.problem.set()


# Функция для обработки ввода описания проблемы
async def problem_input_handler(message: types.Message, state: FSMContext):
    problem = message.text
    await state.update_data(problem=problem)

    # Получаем данные о пользователе и введенном описании проблемы
    user = message.from_user

    data = await state.get_data()
    street = data.get("street")
    house = data.get("house")
    bid_flat = data.get("flat")
    specialist = data.get("specialist")
    bid_address = database.get_address_id(street, house)

    # Сохраняем заявку в базу данных
    database.save_bid_to_database(specialist, bid_address, bid_flat, problem,
                                  user.id)

    # Отправляем сообщение администратору с данными о заявке
    await send_bid_to_admin(user, problem, street, house, bid_flat, specialist)

    # Отправляем сообщение пользователю о принятии заявки
    response_text = f"{user.first_name}, заявку на {specialist} приняли.\n"
    response_text += f"Адрес: {street}, дом {house}, квартира {bid_flat}.\n"
    response_text += f"Проблема: {problem}."
    await message.answer(text=response_text, reply_markup=start_kb)
    await state.finish()



# Функция для отправки заявки администратору
async def send_bid_to_admin(user, problem, street, house, flat, specialist):
    from main import bot
    # Формируем сообщение с данными о заявке
    message_text = f"Новая заявка на {specialist} от @{user.username}.\n"
    message_text += f"Адрес: {street}, дом {house}, квартира {flat}.\n"
    message_text += f"Проблема: {problem}."

    # Отправляем сообщение администратору
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)

##################################
