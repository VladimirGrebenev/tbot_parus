import sqlite3

connection = sqlite3.connect('files/bot_database.db')
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(id INT, username TEXT, first_name TEXT, street TEXT, house_number TEXT, flat_number INT);")
cursor.execute("CREATE TABLE IF NOT EXISTS block(id INT); ")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS our_houses(street TEXT, house_number TEXT); ")

cursor.execute(
    "CREATE TABLE IF NOT EXISTS bids(specialist TEXT, bid_address INT, bid_flat TEXT, problem VARCHAR(255), user_id INT); ")

# Функция создания пользователя
def add_user(user_id, username, first_name):
    # Получаем id пользователя из базы данных
    check_user = cursor.execute('SELECT * FROM Users WHERE id=?', (user_id,))

    # Проверяем есть ли пользователь уже в бд
    if check_user.fetchone() is None:
        # Добавляем пользователя
        cursor.execute(
            f"INSERT INTO Users VALUES('{user_id}', '{username}', '{first_name}', 'street', 'house_number', 0); ")

        # Обновляем таблицу
    connection.commit()

def add_house(street, house_number):
    # Проверяем, существует ли уже такой дом в базе данных
    check_house = cursor.execute('SELECT * FROM our_houses WHERE street=? AND house_number=?', (street, house_number)).fetchone()

    # Если дом уже существует, ничего не делаем
    if check_house is None:
        # Добавляем новый дом в базу данных
        cursor.execute("INSERT INTO our_houses VALUES (?, ?)", (street, house_number))

    # Обновляем соединение с таблицей
    connection.commit()


# Функция для получения списка домов из базы данных
def get_houses():
    # Выполняем запрос к базе данных для получения списка домов
    cursor.execute("SELECT * FROM our_houses ORDER BY street, house_number")
    houses = cursor.fetchall()

    # Формируем список словарей с информацией о домах
    houses_list = []
    for house in houses:
        houses_list.append({
            'street': house[0],
            'house_number': house[1]
        })

    return houses_list


def update_user_street(user_id, street):
    # Устанавливаем новое значение улицы для пользователя
    cursor.execute(f'UPDATE Users SET street = ? WHERE id = ?',
                   (street, input_id))
    # Обновляем соединение с таблицей
    connection.commit()


def update_user_house_number(user_id, house_number):
    # Устанавливаем новое значение номера дома для пользователя
    cursor.execute(f'UPDATE Users SET house_number = ? WHERE id = ?',
                   (house_number, input_id))
    # Обновляем соединение с таблицей
    connection.commit()


def update_user_flat_number(user_id, flat_number):
    # Устанавливаем новое значение номера дома для пользователя
    cursor.execute(f'UPDATE Users SET flat_number = ? WHERE id = ?',
                   (flat_number, input_id))
    # Обновляем соединение с таблицей
    connection.commit()


# Функция вывода пользователей
def show_users():
    # Получаем все столбцы из таблицы в список users_list
    users_list = cursor.execute('SELECT * FROM Users')

    # Создаём переменную в которую будем записывать user_id, username, first_name пользователей
    message = ""

    # Проходимся по элементам списка и записываем их в переменную message
    for users in users_list:
        message += (f"id: {users[0]} @{users[1]} имя: {users[2]}, улица:"
                    f" {users[3]}, д. {users[4]}, кв. {users[5]}\n")

    # Обновляем соединение с таблицей
    connection.commit()

    # Возвращаем переменную, которая будет служить сообщением для отправки при нажатии на кнопку
    return message


def users_id():
    # Получаем все столбцы из таблицы в список users_list
    users_id = cursor.execute('SELECT id FROM Users').fetchall()

    # Обновляем соединение с таблицей
    connection.commit()

    return users_id


# Функция возвращающаяя количество пользователей
def show_statistics():
    # Получаем список в котором записано количество элементов первого столбца таблицы
    count_users = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()

    # Обновляем соединение с таблицей
    connection.commit()

    # Возвращаем значение для отправки
    return count_users[0]


# Функция блокировки пользователей
def add_user_to_block(user_id):
    # Обновляем 0 на 1
    cursor.execute(f"INSERT INTO block VALUES({user_id}); ").fetchall()

    # Обновляем соединение с таблицей
    connection.commit()


# Функция для разблокировки пользователей
def unlock_users(user_id):
    # Обновляем 1 на 0
    cursor.execute(f"DELETE FROM block WHERE id = {user_id}; ").fetchall()

    # Обновляем соединение с таблицей
    connection.commit()


# Функция для проверки пользователя на нахождение в блокировке
def check_block(id):
    # Выбираем значение из столбца block у нужного пользователя
    users_block = cursor.execute("SELECT * FROM block; ").fetchall()

    # Обновляем соединение с таблицей
    connection.commit()

    # Возвращаем значение для обработки
    return (id,) in users_block

# Функция получения списка улиц для кнопок
def get_streets():
    # Выполняем запрос к базе данных для получения списка улиц
    cursor.execute("SELECT DISTINCT street FROM our_houses ORDER BY street")
    streets = cursor.fetchall()
    streets = [street[0] for street in streets]
    return streets


# Функция получения списка домов по улице для кнопок
def get_houses_for_steet(street):
    # Выполняем запрос к базе данных для получения списка домов на указанной улице
    cursor.execute("SELECT house_number FROM our_houses WHERE street = ? ORDER BY house_number", (street,))
    houses = cursor.fetchall()
    houses = [houses[0] for houses in houses]
    return houses

# Запись заявки в таблицу bids
def save_bid_to_database(specialist, bid_address, bid_flat, problem, user_id):

    # Запись данных в таблицу "bids"
    cursor.execute("INSERT INTO bids (specialist, bid_address, bid_flat, problem, user_id) VALUES (?, ?, ?, ?, ?)", (specialist, bid_address, bid_flat, problem, user_id))

    # Сохранение изменений и закрытие соединения с базой данных
    connection.commit()

# Функция получения id адреса из таблицы our_houses
def get_address_id(street, house_number):
    # Выполняем запрос к базе данных для получения id адреса по улице и номеру дома
    cursor.execute("SELECT rowid FROM our_houses WHERE street = ? AND house_number = ?", (street, house_number))
    address_id = cursor.fetchone()

    # Обновляем соединение с таблицей
    connection.commit()

    # Возвращаем id адреса
    return address_id[0] if address_id else None