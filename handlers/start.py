from keyboards import *
import database
import texts.start
import texts.admin


async def start(message):
    username = message.from_user.username
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    database.add_user(user_id, username, first_name)
    await message.answer(
        f'✅ Добрый день, {first_name}!\n\n' + texts.start.start,
        reply_markup=start_kb)


async def about_company(message):
    first_name = message.from_user.first_name
    await message.answer(f'<b>{first_name}, выберите что Вас интересует:</b>',
                         parse_mode='HTML', reply_markup=about_company_kb)


async def call_our_houses_callback(call):
    # Получаем список домов из базы данных
    houses = database.get_houses()

    # Формируем сообщение со списком домов
    message_text = f"<b>Список наших домов:</b>\n"
    for house in houses:
        message_text += f"- {house['street']}, {house['house_number']}\n"

    # Отправляем сообщение со списком домов
    await call.message.answer(message_text, parse_mode='HTML')

async def call_about_us(call):
    await call.message.answer(texts.start.about_us, parse_mode='HTML',
                              reply_markup=about_company_kb)
    await call.answer()


async def call_requisites(call):
    await call.message.answer(texts.start.requisites, parse_mode='HTML',
                              reply_markup=about_company_kb)
    await call.answer()


async def call_license(call):
    with open("images/sert_1.jpg", "rb") as img:
        # Отправляем изображение вместе с текстом
        await call.message.answer_photo(img, texts.start.license_text,
                                        parse_mode='HTML',
                                        reply_markup=about_company_kb)
        await call.answer()


async def call_company_contacts(call):
    await call.message.answer(texts.start.company_contacts, parse_mode='HTML',
                              reply_markup=about_company_kb)
    await call.answer()


async def ban_message(update):
    await update.answer(texts.admin.ban, parse_mode='HTML')


async def ban_callbackquery(update):
    await update.message.answer(texts.admin.ban, parse_mode='HTML')
    await update.answer()
