# About TBOT_PARUS
Телеграм бот для управляющей компании, для взаимодействия с жильцами домов:
- статичная информация
- подача заявки на специалистов
- запись к директору на приём
Админка бота:
- выдача и снятие банов
- статистика пользователей
- добавление новых домов
- рассылка подписчикам

# Stack
- Python 3.10
- aiofiles==23.2.1
- aiogram==2.23.1
- google-auth==2.27.0
- gspread==6.0.2
- requests==2.31.0
и т.д. -> requirements.txt

# To start working development DRF

1. стяни ветку мастер - pull master from github
2. не забудь установить зависимости pip install -r requirements.txt
3. создай файл config.py с настройками бота на основе config_sample.py
4. создай бота в телеграм @BotFather, добавь в config.py
5. создай Google API https://console.developers.google.com/ и google sheets (для записи к директору), добавь в config.py
6. добавь администратор в config.py
7. запусти main.py
8. наполни базу домами в админке телеграмм, для старта админки /admin
9. для старта бота в телеграм /start
  

# TODO:
- сделать базу данных Postgres
- сделать API для бота
- сделать SPA на React с расширенным функционалом для пользователей и админа
