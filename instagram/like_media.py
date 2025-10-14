import time
import random

from instagram.bd import write_is_like_to_db
from instagram.save_session import save_session
from login import set_login
from config import SLEEP_BETWEEN, SESSION_FILE
from config import log
from instagrapi import Client
from bd import read_usernames_from_bd


def like_latest_media_of(username: str, cl: Client) -> bool:
    """
    Ставит лайк на последней медиа пользователя username.
    Возвращает True при успехе, False при неудаче или если нет медиа.
    """
    time.sleep(20)
    log.info("Processing user: %s", username)
    try:
        user = cl.user_info_by_username(username)
        print(f"Юзер - {user}")
    except Exception as e:
        log.error("Failed to get user info for %s: %s", username, e)
        return False

    data = cl.private_request(f"feed/user/{user.pk}/", params={"count": 1})
    items = data.get("items", [])
    print(items)

    if items:
        media_id = items[0]["id"]  # тут сразу нужный id
        cl.media_like(media_id)
        print("Поставил лайк 👍")
        return True
    else:
        print("Нет постов у пользователя")
        return False


def main():
    count = 0
    cl = set_login()  # Залогиниваемся
    target_usernames = read_usernames_from_bd(5, is_like=True)
    success_usernames = []
    print(target_usernames)

    for username in target_usernames:
        try:
            success = like_latest_media_of(username, cl)
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

if __name__ == "__main__":
    main()
