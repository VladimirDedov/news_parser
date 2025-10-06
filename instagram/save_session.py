from instagrapi import Client
from config import SESSION_FILE
from config import log


def save_session(cl: Client):
    # Сохраняем сессию
    try:
        cl.dump_settings(SESSION_FILE)
        log.info("Session saved.")
    except Exception as e:
        log.warning(f"Failed to dump session: {e}")
