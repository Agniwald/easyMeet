import os
from dotenv import load_dotenv

load_dotenv()

MAIL = os.environ.get("MAIL")
PASSWORD = os.environ.get("PASSWORD")
DB_URI = os.environ.get("DB_URI")
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
# FIREFOX_BIN = os.environ.get("FIREFOX_BIN")
# GECKODRIVER_PATH = os.environ.get("GECKODRIVER_PATH")
