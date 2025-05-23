import sqlite3


def write_to_bd(list_of_data: list):
    flag = True
    try:
        with sqlite3.connect('nurkz.db') as conn:  # connected for sd.db or create BD
            cur = conn.cursor()  # for sql requests in BD
            cur.execute("""
                CREATE TABLE IF NOT EXISTS nurkz (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_article TEXT,
                    url_article TEXT,
                    title_original_article TEXT,
                    text_original_article TEXT,
                    title_neiro_article TEXT DEFAULT NULL,
                    text_neiro_article TEXT DEFAULT NULL,
                    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_published BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()
    except:
        print("Не удалось подключиться или создать БД")

    try:
        cur.execute("INSERT INTO nurkz(id_article, url_article, title_original_article, "
                    "text_original_article) VALUES(?,?,?,?)",
                    tuple(list_of_data))
        conn.commit()
    except:
        print("Не удалось записать данные")


def read_from_bd():
    pass
