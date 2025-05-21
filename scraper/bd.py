import sqlite3
from datetime import datetime

def write_to_bd(list_of_data: list):
    flag = True
    try:
        conn = sqlite3.connect('nurkz.db')  # connected for sd.db or create BD
        cur = conn.cursor()  # for sql requests in BD
        cur.execute("""
            CREATE TABLE IF NOT EXISTS nurkz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_article TEXT,
                url_article TEXT,
                title_article TEXT,
                text_article TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except:
        flag = False
        print("Не удалось подключиться или создать БД")

    conn.commit()

    cur.execute("INSERT INTO nurkz(id_article, url_article, title_article, text_article) VALUES(?,?,?,?)", tuple(list_of_data))
    conn.commit()
