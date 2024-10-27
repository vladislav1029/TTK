import sqlite3
access=0
import json
import random

def generate_random_temp_doc():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])
def import_bd(registration_username, registration_password, access):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    a = registration_username
    b = registration_password
    c = access
    temp_doc = generate_random_temp_doc()

    query1 = f"INSERT INTO registration (number, email, access, temp_doc) VALUES('{a}', '{b}', '{c}', '{temp_doc}')"
    cur.execute(query1)
    con.commit()
    cur.close()
    con.close()
    return temp_doc  # Возвращаем сгенерированный временный код


#добавление редактора в базу данных
def import_redactor_bd(redactor_username, redactor_password, redactor_access):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    a = redactor_username
    b = redactor_password
    c=redactor_access
    query1 = f" INSERT INTO admin_user (login,password,access) VALUES('{a}','{b}','{c}' )"
    cur.execute(query1)
    con.commit()
    cur.close()
    con.close()


#проверка клиента в базе данных
def check_user_bd(entrance_password):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    query = f"SELECT * FROM registration WHERE number_doc='{entrance_password}' OR temp_doc='{entrance_password}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[3] == 1:  # Проверяем значение столбца access (индекс 2 в кортеже)
            print("нашел клиента с договором")
            return True  # Возвращаем 'kbuser', если access равен 1

        else:
            print("нашел клиента без договора")
            return False  # Возвращаем 'kbnewuser', если access равен 0

    return None  # Возвращаем None, если пользователя не существует


#проверка тарифа в базе данных
def check_tariff_bd(tariff):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    query = f"SELECT * FROM tariff WHERE tariff='{tariff}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[2] == 2:  # Проверяем значение столбца access (индекс 2 в кортеже)
            print("максимальный")
            return "max"  # Возвращаем 'max', если category равен 1
        elif result[2]==1:
            print("мощный")
            return "norm"  # Возвращаем 'norm', если category равен 1

        else:
            print("честный")
            return "min"  # Возвращаем 'min', если category равен 0

    return None  # Возвращаем None, если тарифа не существует

#добавляем тариф клиенту
def change_tarif_client(tariff, number): #амени
    conn = sqlite3.connect('ttk.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE registration SET tariff = '{tariff}' WHERE number='{number}' "
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()



#проверка услуги в базе данных
def check_service_bd(service):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    query = f"SELECT * FROM service WHERE service='{service}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[2] == 3:  # Проверяем значение столбца access (индекс 2 в кортеже)
            print("антивирус касперский")
            return "antivirus"  # Возвращаем 'max', если category равен 1
        elif result[2]==2:
            print("персональный менеджер")
            return "manager"  # Возвращаем 'norm', если category равен 1
        elif result[2]==1:
            print("выделенный ip")
            return "ip"  # Возвращаем 'norm', если category равен 1

        else:
            print("фирменный роутер")
            return "router"  # Возвращаем 'min', если category равен 0

    return None  # Возвращаем None, если тарифа не существует

#добавляем услугу клиенту
def change_service_client(service_id, username):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Получаем текущий список услуг клиента
    cur.execute(f"SELECT service FROM registration WHERE number='{username}'")
    result = cur.fetchone()

    if result:
        services = json.loads(result[0]) if result[0] else []
    else:
        services = []

    # Добавляем новую услугу в список, если её там ещё нет
    if service_id not in services:
        services.append(service_id)

    # Обновляем список услуг в базе данных
    cur.execute(f"UPDATE registration SET service=? WHERE number=?", (json.dumps(services), username))

    con.commit()
    cur.close()
    con.close()


def get_user_tariff_and_services(username):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    query = "SELECT tariff, service FROM registration WHERE number=?"
    cur.execute(query, (username,))
    result = cur.fetchone()

    cur.close()
    con.close()

    if result:
        tariff = result[0]
        services = json.loads(result[1]) if result[1] else []
        print(f"Tariff: {tariff}, Services: {services}")  # Отладочное сообщение
        return tariff, services
    else:
        print("No data found for user")  # Отладочное сообщение
        return "Неизвестно", []
def check_admin_bd(entrance_username, entrance_password):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    query = f"SELECT * FROM admin_user WHERE login='{entrance_username}' AND password='{entrance_password}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[3] == 1:  # Проверяем значение столбца access (индекс 2 в кортеже)
            return True  # Возвращаем 'kbadmin', если access равен 1
        else:
            return False  # Возвращаем 'kbredactor', если access равен 0

    return None  # Возвращаем None, если пользователя не существует

def check_admin(entrance_username, ):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    query = f"SELECT * FROM admin_user WHERE login='{entrance_username}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    return None  # Возвращаем None, если пользователя не существует


def delete_redactor_bd(login):
    conn = sqlite3.connect('ttk.db')
    cursor = conn.cursor()

    # Используем параметризованный запрос для безопасности
    cursor.execute("DELETE FROM admin_user WHERE login=?", (login,))

    conn.commit()
    cursor.close()
    conn.close()

def find_category(message_text):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Разбиваем сообщение на слова
    words = message_text.split()

    # Ищем каждое слово в таблице request
    for word in words:
        query = "SELECT category FROM request WHERE intention=?"
        cur.execute(query, (word,))
        result = cur.fetchone()

        if result:
            category = result[0]
            cur.close()
            con.close()
            return str(category)

    cur.close()
    con.close()
    return None  # Если ключевые слова не найдены

def add_category(category_name, words):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Добавляем категорию в таблицу category
    cur.execute("INSERT INTO category (name) VALUES (?)", (category_name,))
    category_id = cur.lastrowid

    # Добавляем ключевые слова в таблицу request
    for word in words:
        cur.execute("INSERT INTO request (intention, category) VALUES (?, ?)", (word, category_id))

    con.commit()
    cur.close()
    con.close()

def edit_category(category_name, words):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Удаляем все ключевые слова для данной категории
    cur.execute("DELETE FROM request WHERE category=?", (category_name,))

    # Добавляем новые ключевые слова
    for word in words:
        cur.execute("INSERT INTO request (intention, category) VALUES (?, ?)", (word, category_name))

    con.commit()
    cur.close()
    con.close()

def delete_category(category_name):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Удаляем все ключевые слова для данной категории
    cur.execute("DELETE FROM request WHERE category=?", (category_name,))

    # Удаляем категорию
    cur.execute("DELETE FROM category WHERE name=?", (category_name,))

    con.commit()
    cur.close()
    con.close()
