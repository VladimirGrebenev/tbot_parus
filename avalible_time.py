import gspread
from datetime import datetime, timedelta
import config

# Подключение к Google Sheets
gc = gspread.service_account(filename=config.google_sheets_file_key)
#Открываем google нашу таблицу
sh = gc.open("Запись к директору")
# выбираем лист
worksheet = sh.sheet1



def get_avalible_time():
    # Ищем ближайший четверг
    next_thursday = get_next_thursday()
    print(next_thursday.strftime('%d.%m.%Y'))

    # Ищем ячейку с ближайшим четвергом
    date_range = worksheet.range('A2:A46')
    thursday_cell = None
    for cell in date_range:
        if cell.value == next_thursday.strftime('%d.%m.%Y'):
            thursday_cell = cell
            break

    print(thursday_cell)
    if thursday_cell is None:
        return None

    # Ищем свободные ячейки в диапазоне времени
    time_range = worksheet.range('B1:M1')
    available_times = []
    for i, time_cell in enumerate(time_range):
        date_cell = worksheet.cell(thursday_cell.row, time_cell.col)
        print(f'date_cell: {date_cell} \n')
        if date_cell.value == None:
            available_times.append(time_range[i].value)

    return available_times

def get_next_thursday():
    today = datetime.today()
    days_ahead = (3 - today.weekday()) % 7
    next_thursday = today + timedelta(days=days_ahead)
    return next_thursday


print(get_avalible_time())