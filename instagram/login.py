import logging
import os

from instagrapi import Client
from config import TEST_LOGIN, INST_PASS

USERNAME = TEST_LOGIN
PASSWORD = INST_PASS
SESSION_FILE = "session.json"  # файл для сохранения сессии
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def set_login():
    """Если есть сессия сохраненная, то загружаем её. Если нет, то логинимся по логину - паролю"""
    cl = Client()
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            log.info("Loaded session settings.")
        # try to ensure session valid; if not, login
        try:
            # quick request to check session validity
            cl.account_info()
            log.info("Session is valid.")
        except Exception:
            log.info("Session not valid or not logged — logging in using credentials.")
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            log.info("Logged in and saved session.")
    except Exception as e:
        log.exception("Session load/login failed — attempting fresh login.")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        log.info("Logged in and saved session after failure.")

    return cl
