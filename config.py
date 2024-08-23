import os

from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL", default="")
MAX_FILE_SIZE = os.getenv("MAX_FILE_SIZE", default=25)  # MB
REFRESH_URL_BOT_TOKEN = os.getenv("REFRESH_URL_BOT_TOKEN", default="")
REFRESH_URL_API = os.getenv("REFRESH_URL_API", default="")
SENTRY_DSN = os.getenv("SENTRY_DSN", default="")
