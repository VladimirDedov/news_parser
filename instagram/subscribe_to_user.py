import time
import random
from login import set_login
from config import SLEEP_BETWEEN
from bd import read_usernames_from_bd, write_subscribes_to_db
from instagrapi import Client
from save_session import save_session


def follow_user(username: str, cl: Client)-> bool:
    """Подпись на пользователя по username"""

    # Найдём пользователя по нику
    user = cl.user_info_by_username(username)

    # Подписка на пользователя
    is_success = cl.user_follow(user.pk)
    print(f"Подписался на {user.username}")
    return is_success


if __name__ == '__main__':
    cl = set_login()  # Залогиниваемся
    target_usernames = read_usernames_from_bd(3, is_subscribe=True)#Получаем пользователей на кого подписаться
    success_usernames = []
    sent_request_usernames = []
    print(target_usernames)

    for username in target_usernames:
        try:
            is_success = follow_user(username, cl)
            if is_success:
                success_usernames.append(username)
            else:
                sent_request_usernames.append(username)
        except Exception as e:
            print(f"ошибка - {e}")
            continue

        # небольшая пауза между пользователями, чтобы не выглядеть роботом
        time.sleep(random.randint(SLEEP_BETWEEN, SLEEP_BETWEEN * 2))

    print(f"Подписался на  {len(success_usernames)} человек")
    print(f"Отправил запрос  {len(sent_request_usernames)} человек")

    # Сохраняем пользователей, на кого успегно подписались
    write_subscribes_to_db([(st,) for st in success_usernames])

    # Сохраняем пользователей, кому отправили запрос поле в БД(is_sent_request)
    write_subscribes_to_db([(st,) for st in sent_request_usernames], is_sent_request=True)

    # Сохраняем сессию
    save_session(cl)