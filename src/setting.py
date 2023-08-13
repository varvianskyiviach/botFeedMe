from os import getenv
from pathlib import Path

SRC_FOLDER = Path(__file__).parent
ROOT_FOLDER = SRC_FOLDER.parent

DATABASE_NAME = getenv("DATABASE_NAME", default="db")

TELEGRAM_BOT_API_KEY = getenv("TELEGRAM_BOT_API_KEY")
