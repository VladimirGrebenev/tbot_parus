from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📝 Услуги'),
            KeyboardButton(text='ℹ️ О нас'),
        ],
        [
            KeyboardButton(text='👨‍💼 Запись к директору')
        ],
    ], resize_keyboard=True
)

about_company_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Раскрытие информации',
                                 callback_data='Раскрытие информации'),
        ],
        [
            InlineKeyboardButton(text='Наши дома',
                                 callback_data='our_houses'),
        ],
        [
            InlineKeyboardButton(text='Реквизиты',
                                 callback_data='Реквизиты'),
            InlineKeyboardButton(text='Лицензии',
                                 callback_data='Лицензии'),
            InlineKeyboardButton(text='Контакты',
                                 callback_data='Контакты'),
        ],
    ]
)

services_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👨‍🔧 Сантехник',
                                 callback_data='Сантехник'),
        ],
        [
            InlineKeyboardButton(text='👷‍♀️ Электрик',
                                 callback_data='Электрик'),
        ],
        [
            InlineKeyboardButton(text='🛠️ Прочие услуги',
                                 callback_data='Прочие услуги'),
        ],
    ]
)

send_bid_plumber_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📨 Отправить заявку",
                                 callback_data='заявка на сантехника'),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="back_to_services"),
        ],
    ]
)

send_bid_electrician_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📨 Отправить заявку",
                                 callback_data='заявка на электрика'),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="back_to_services"),
        ],
    ]
)

admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✉️ Рассылка", callback_data="mailing"),
        ],
        [
            InlineKeyboardButton(text="🏢 Добавить дом",
                                 callback_data="add_house"),
        ],
        [
            InlineKeyboardButton(text="👨‍👩‍👦‍👦 Пользователи",
                                 callback_data="users"),
        ],
        [
            InlineKeyboardButton(text="📊 Статистика",
                                 callback_data="statistics"),
        ],
        [
            InlineKeyboardButton(text="⛔️ Блокировка",
                                 callback_data="block_user"),
            InlineKeyboardButton(text="✅ Разблокировка",
                                 callback_data="unlock_user"),
        ],
    ]
)

back_to_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="back_to_admin"),
        ],
    ]
)

