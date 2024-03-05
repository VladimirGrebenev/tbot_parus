# Импортируем все необходимые модули
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

# импортируем конфиги, функции базы данных
import config
import database

# импортируем хендлеры
import handlers.start
import handlers.services
import handlers.admin
import handlers.director_appointment
import handlers.service_bid

# --------------------------------------------------------#
# создаём бота через API токен
api = config.API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
# --------------------------------------------------------#

# регистрируем хендлеры
# обработчики пользователей попавших в бан
dp.message_handler(lambda m: database.check_block(m.from_user.id))(
    handlers.start.ban_message)
dp.callback_query_handler(lambda c: database.check_block(c.from_user.id))(
    handlers.start.ban_callbackquery)

# start.py хендлеры
dp.message_handler(commands=['start'])(handlers.start.start)
dp.message_handler(Text(equals=['ℹ️ О нас']))(handlers.start.about_company)
dp.callback_query_handler(text='Раскрытие информации')(
    handlers.start.call_about_us)
dp.callback_query_handler(text="our_houses")(
    handlers.start.call_our_houses_callback)
dp.callback_query_handler(text='Реквизиты')(handlers.start.call_requisites)
dp.callback_query_handler(text='Лицензии')(handlers.start.call_license)
dp.callback_query_handler(text='Контакты')(
    handlers.start.call_company_contacts)

# services.py хендлеры
dp.message_handler(Text(equals=['📝 Услуги']))(handlers.services.uk_services)
dp.callback_query_handler(text='Сантехник')(handlers.services.call_plumber)
dp.callback_query_handler(text='Электрик')(handlers.services.call_electrician)
dp.callback_query_handler(text='back_to_services')(
    handlers.services.call_back_to_services)

# service_bid.py хендлеры
dp.callback_query_handler(text='заявка на сантехника')(
    handlers.service_bid.call_bid_plumber)
dp.callback_query_handler(text='заявка на электрика')(
    handlers.service_bid.call_bid_electrician)
dp.callback_query_handler(text='Прочие услуги')(
    handlers.service_bid.call_bid_other)
dp.callback_query_handler(state=handlers.service_bid.PlumberState.street)(
    handlers.service_bid.call_street_selected)
dp.callback_query_handler(state=handlers.service_bid.PlumberState.house)(
    handlers.service_bid.call_house_selected)
dp.message_handler(state=handlers.service_bid.PlumberState.flat)(
    handlers.service_bid.flat_input_handler)
dp.message_handler(state=handlers.service_bid.PlumberState.problem)(
    handlers.service_bid.problem_input_handler)

# admin.py хендлеры
dp.message_handler(commands=['admin'])(handlers.admin.admin_entry)
dp.callback_query_handler(text='users')(handlers.admin.call_users)
dp.callback_query_handler(text='statistics')(handlers.admin.call_statistics)
dp.callback_query_handler(text='block_user')(handlers.admin.call_ban_user)
dp.message_handler(state=handlers.admin.AdminState.BAN)(
    handlers.admin.add_to_ban)
dp.callback_query_handler(text="back_to_admin")(handlers.admin.call_back_admin)
dp.callback_query_handler(text='unlock_user')(handlers.admin.call_unlock_user)
dp.message_handler(state=handlers.admin.AdminState.UNBAN)(
    handlers.admin.unban)
dp.callback_query_handler(text="add_house")(
    handlers.admin.call_add_house_callback)
dp.message_handler(state=handlers.admin.AdminState.ADD_HOUSE)(
    handlers.admin.process_add_house)
dp.callback_query_handler(text="mailing")(handlers.admin.mailing)
dp.message_handler(state=handlers.admin.AdminState.mailing_step1)(
    handlers.admin.mailing1)
dp.message_handler(content_types=types.ContentTypes.PHOTO,
                   state=handlers.admin.AdminState.mailing_step2)(
    handlers.admin.mailing2)

# director_appointment.py / запись к директору
dp.message_handler(Text(equals=['👨‍💼 Запись к директору']))(
    handlers.director_appointment.handle_director_appointment)
dp.message_handler(state=handlers.director_appointment
                   .DirectorAppointmentStates.QUESTION)(
    handlers.director_appointment.handle_question)
dp.callback_query_handler(state=handlers.director_appointment
                          .DirectorAppointmentStates.APPOINTMENT_TIME)(
    handlers.director_appointment.handle_appointment_time)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
