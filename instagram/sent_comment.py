
import time
import random

from instagram.bd import write_is_like_to_db
from login import set_login
from config import SLEEP_BETWEEN,SESSION_FILE
from config import log
from bd import read_usernames_from_bd
from instagrapi import Client
from save_session import save_session

def put_comment(username: str, cl: Client):
    """Оставить коментарии под последней публикацией"""
    text_comment = "Прикол!"
    # Получаем ID пользователя
    user = cl.user_info_by_username(username)

    # Забираем последние посты напрямую через private_request
    data = cl.private_request(f"feed/user/{user.pk}/", params={"count": 1})
    items = data.get("items", [])
    print(items)
    if items:
        media_id = items[0]["id"]  # ID последнего поста
        cl.media_comment(media_id, text_comment)
        print(f"✅ Комментарий '{text_comment}' оставлен под последним постом {username}")
    else:
        print(f"❌ У пользователя {username} нет публикаций")

def main():
    count = 0
    cl = set_login()  # Залогиниваемся
    target_usernames = read_usernames_from_bd(25, is_comment=True)
    success_usernames = []
    print(target_usernames)

    for username in target_usernames:
        try:
            success = put_comment(username, cl)
            if success:
                count += 1
                success_usernames.append(username)
        except Exception as e:
            print(f"ошибка - {e}")
            continue
        # success= put_comment(username, cl)
        # небольшая пауза между пользователями, чтобы не выглядеть роботом
        time.sleep(random.randint(SLEEP_BETWEEN, SLEEP_BETWEEN * 2))
    print(f"Поставлено {count} лайкосов")

    # Сохраняем пользователей, кому пытались ставить лайк на пост
    write_is_like_to_db([(st,) for st in target_usernames])

    # Сохраняем пользователей, кому успешно поставился лайк на пост
    write_is_like_to_db([(st,) for st in success_usernames], is_like_success=True)

    # Сохраняем сессию
    save_session(cl)