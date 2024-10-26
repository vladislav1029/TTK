import sqlite3
access=0


#добавление клиента в базу данных
def import_bd(registration_username, registration_password):
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()
    a = registration_username
    b = registration_password
    c=access
    query1 = f" INSERT INTO registration (login,password,access) VALUES('{a}','{b}','{c}' )"
    cur.execute(query1)
    con.commit()
    cur.close()
    con.close()


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
    query = f"SELECT * FROM registration WHERE password='{entrance_password}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[3] == 1:  # Проверяем значение столбца access (индекс 2 в кортеже)
            print("нашел клиента с договором")
            return "kbuser"  # Возвращаем 'kbuser', если access равен 1

        else:
            print("нашел клиента без договора")
            return "kbnewuser"  # Возвращаем 'kbnewuser', если access равен 0

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
    sql_query = f"UPDATE registration SET tariff = '{tariff}' WHERE login='{number}' "
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
def change_service_client(service, number): #амени
    conn = sqlite3.connect('ttk.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE registration SET service = '{service}' WHERE login='{number}' "
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


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
            return "kbadmin"  # Возвращаем 'kbadmin', если access равен 1
        else:
            return "kbredactor"  # Возвращаем 'kbredactor', если access равен 0

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