import sqlite3

def create_db():
    con = sqlite3.connect('ttk.db')
    cur = con.cursor()

    # Создаем таблицу registration
    cur.execute('''
        CREATE TABLE IF NOT EXISTS registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            access INTEGER NOT NULL
        )
    ''')

    con.commit()
    cur.close()
    con.close()

if __name__ == '__main__':
    create_db()