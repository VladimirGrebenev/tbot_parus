from keyboards import *
import texts.services


async def uk_services(message):
    first_name = message.from_user.first_name
    await message.answer(f'<b>{first_name}, выберите услугу:</b>',
                         parse_mode='HTML', reply_markup=services_kb)

async def call_plumber(call):
    await call.message.edit_text(texts.services.plumber, parse_mode='HTML',
                                 reply_markup=send_bid_plumber_kb)
    await call.answer()


async def call_electrician(call):
    await call.message.edit_text(texts.services.electrician, parse_mode='HTML',
                                 reply_markup=send_bid_electrician_kb)
    await call.answer()


async def call_back_to_services(call):
    await call.message.edit_text(
        f'<b>Выберите услугу:</b>',
        parse_mode='HTML', reply_markup=services_kb)
    await call.answer()
