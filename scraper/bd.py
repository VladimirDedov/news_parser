import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection(db_name: str = "nurkz.db"):  # Подключение к БД
    conn = sqlite3.connect(db_name)
    try:
        cur = conn.cursor()

        # ⬇️ Создание таблицы при первом подключении
        cur.execute("""
                CREATE TABLE IF NOT EXISTS nurkz (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_article TEXT,
                    url_article TEXT,
                    url_image TEXT DEFAULT NULL,
                    image_path TEXT DEFAULT NULL,
                    image_text TEXT DEFAULT NULL,
                    title_original_article TEXT,
                    text_original_article TEXT,
                    title_neiro_article TEXT DEFAULT NULL,
                    text_neiro_article TEXT DEFAULT NULL,
                    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_published BOOLEAN DEFAULT FALSE
                )
            """)
        yield cur
        conn.commit()
    except Exception as err:
        print(f"Не удалось подключиться или создать БД\n {err}")


def write_to_bd(list_of_data: list):
    with get_db_connection("nurkz.db") as cur:
        if len(list_of_data) > 2:
            try:
                cur.execute("INSERT INTO nurkz(id_article, url_article, title_original_article, "
                            "text_original_article) VALUES(?,?,?,?)",
                            tuple(list_of_data))
            except Exception as err:
                print(f"Не удалось записать данные\n {err}")
        else:
            try:
                cur.execute("INSERT INTO nurkz(image_text, title_neiro_article, text_neiro_article) "
                            "VALUES(?,?)",
                            tuple(list_of_data))
            except Exception as err:
                print(f"Не удалось записать данные\n {err}")


def read_from_bd_origin_article(id_article):
    try:
        with sqlite3.connect('nurkz.db') as conn:  # connected for sd.db or create BD
            cur = conn.cursor()  # for sql requests in BD
            cur.execute("""
                SELECT title_original_article, text_original_article from nurkz
                WHERE id_article = id_article
            """)
            result = cur.fetchone()  # Или fetchall() — если ожидается несколько строк
            return result
    except:
        print("Не удалось подключиться или создать БД")
