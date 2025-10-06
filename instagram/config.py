import os
import logging
from dotenv import load_dotenv
load_dotenv()

INST_LOGIN = os.getenv("INST_LOGIN")
TEST_LOGIN = os.getenv("TEST_LOGIN")
INST_PASS = os.getenv("INST_PASS")

TARGET_USERNAMES=["program_files_86"]
SLEEP_BETWEEN = 3
SESSION_FILE = "session.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)