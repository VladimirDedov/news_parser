import sqlite3
from contextlib import contextmanager
from .bd_create import create_table


@contextmanager
def get_db_connection(db_name: str = "nurkz.db"):
    """Подключение к БД"""
    conn = sqlite3.connect(db_name)
    try:
        cur = conn.cursor()
        create_table(cur)#Если таблиц нет, то создать
        yield cur
        conn.commit()
    except Exception as err:
        print(f"Не удалось подключиться или создать БД\n {err}")
        conn.rollback()
    finally:
        conn.close()

def write_article_to_bd(list_of_data: list, id_article: str = None, original: bool = True):
    """Запись в базу данных информации о статье. Если статья оригинальная, то флаг original = True
    Если статья обработана ИИ, то флаг original = False"""

    with get_db_connection("nurkz.db") as cur:
        if original:
            try:
                cur.execute("INSERT OR IGNORE INTO article(id_article, url_article, title_original_article, "
                            "text_original_article) VALUES(?,?,?,?)"                            ,
                            tuple(list_of_data))
                if cur.rowcount == 0:
                    print(f"{list_of_data[2]} - Статья уже была, пропускаем.")
                else:
                    print(f"Добавлена новая статья - {list_of_data[2]}")

            except Exception as err:
                print(f"Не удалось записать данные\n {err}")
        else:
            try:
                cur.execute(
                    "UPDATE article "
                    "SET title_neiro_article = :title, text_neiro_article = :text, prompt_image = :prompt "
                    "WHERE id_article = :id",
                    {
                        'title': list_of_data[0],
                        'text': list_of_data[1],
                        'prompt': list_of_data[2],
                        'id': id_article
                    }
                )

            except Exception as err:
                print(f"Не удалось записать данные\n {err}")

def write_image_to_bd(list_of_data: list):
    with get_db_connection() as cur:
        cur.execute(
            "INSERT OR IGNORE INTO image(id_article, image_path, image_path_with_text, image_text)"
                "VALUES(?,?,?,?)",
                tuple(list_of_data)
        )

def read_from_bd_origin_article(id_article: str):
    try:
        with get_db_connection("nurkz.db") as cur:  # connected for sd.db or create BD
            cur.execute("""
                SELECT id_article, title_original_article, text_original_article from article
                WHERE id_article = id_article AND is_published = 0
            """)
            result = cur.fetchone()  # Или fetchall() — если решу делать в несколько строк
            return result
    except:
        print("Не удалось подключиться или создать БД")
