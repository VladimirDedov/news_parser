import sqlite3
import time
from typing import List, Dict, Any, Tuple

AMOUNT = 0  # 0 или None = все подписчики
BATCH_SIZE = 50  # сколько пользователей сохранять перед паузой
SLEEP_BETWEEN = 5  # пауза между пачками (секунд)


def connect_db():
    conn = sqlite3.connect("/home/vvv/Python/instagram/followers.db")
    cursor = conn.cursor()
    return cursor, conn


# ==== Instagram ====
def write_subscribe_to_bd(followers: List[Tuple[Any]]):
    cur, conn = connect_db()

    print("Начинаю запись в БД")

    try:
        cur.executemany("""
                        INSERT OR IGNORE INTO followers (pk, username, full_name, is_private)
                        VALUES (?, ?, ?, ?)
                    """, followers
                        )
    except Exception as e:
        print(e)
        print(f"Не удалось записать пиздюков в базу данных")

    conn.commit()

    print(f"✅ Сохранено {len(followers)} подписчиков , пауза {SLEEP_BETWEEN} сек...")
    time.sleep(SLEEP_BETWEEN)

    conn.close()


def get_progress(username: str) -> int:
    """Берём последний обработанный индекс из таблицы progress"""
    cur, conn = connect_db()
    cur.execute("SELECT last_cursor FROM progress WHERE username = ?", (username,))
    row = cur.fetchone()
    return row[0] if row else -1


def save_progress(username: str, last_cursor: int):
    """Сохраняем прогресс парсинга пользователей (последняя страница пагинации) в БД"""
    cur, conn = connect_db()
    cur.execute("""
        INSERT OR REPLACE INTO progress (username, last_cursor)
VALUES (?, ?);
    """, (username, last_cursor))
    conn.commit()
    conn.close()


def read_usernames_from_bd(number_users: int = 1, is_like=False, is_subscribe=False, is_comment=False) -> List[str]:
    """Если is_like выбираем пользователей для постановки Лайка ему на последний пост, если его еще не лайкали
    Если is_subscribe = True, то выбираются пользователя для подписки на них
    """
    cur, conn = connect_db()
    if is_like:
        cur.execute("SELECT username FROM followers WHERE is_like=0 LIMIT ?", (number_users,))
    elif is_subscribe:
        cur.execute("SELECT username FROM followers WHERE is_subscribe=0 and is_sent_request=0 LIMIT ?",
                    (number_users,))
    elif is_subscribe:
        cur.execute("SELECT username FROM followers WHERE is_like_success=1 and is_comment=0 LIMIT ?",
                    (number_users,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows] if rows else []


def write_is_like_to_db(usernames: List[Tuple[str]], is_like_success: bool = False):
    """Проставляет поле is_like в 1 для выбранных пользователей(что пользователь обрабатывался на лайк посту),
    is_like_succes в 1 (если есть хоть один пост и лайк успешно поставлен)"""
    cur, conn = connect_db()

    if is_like_success:
        try:
            cur.executemany("UPDATE followers SET is_like_success = 1 WHERE username = ?", usernames)
            print("Единички поля is_like_success проставлены")
        except Exception as e:
            print(e)
            print("Чет единички поля is_like_success не проставились. смотри write_is_like_success_to_db")
    else:
        try:
            cur.executemany("UPDATE followers SET is_like = 1 WHERE username = ?", usernames)
            print("Единички поля is_like проставлены")
        except Exception as e:
            print(e)
            print("Чет единички поля is_like не проставились. смотри write_like_to_db")

    conn.commit()
    conn.close()


def write_subscribes_to_db(usernames: List[Tuple[str]], is_sent_request: bool = False):
    """Проставляет поле is_subscribe в 1 для выбранных пользователей, что на него удачно подписалось,
    is_sent_request в 1, если был отправлен запрос на подписку"""
    cur, conn = connect_db()
    if is_sent_request:
        try:
            cur.executemany("UPDATE followers SET is_sent_request = 1 WHERE username = ?", usernames)
            print("Единички поля is_sent_request проставлены")
        except Exception as e:
            print(e)
            print("Чет единички поля is_sent_request не проставились. смотри write_subscribes_to_db")
    else:
        try:
            cur.executemany("UPDATE followers SET is_subscribe = 1 WHERE username = ?", usernames)
            print("Единички поля is_subscribe проставлены")
        except Exception as e:
            print(e)
            print("Чет единички поля is_subscribe не проставились. смотри write_subscribes_to_db")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    cur, conn = connect_db()
    print(read_usernames_from_bd(2, is_subscribe=True))
    users = read_usernames_from_bd(2)


    # write_is_like_to_db([('aiden82932',)])
    # write_is_like_success_to_db([('aiden82932',)])
    # write_subscribe_to_bd([(1, "test", "testov", False)])
    # создаём таблицу (если ещё нет)
    # cur.execute("""

    # conn.commit()
