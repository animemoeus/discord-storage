import os

from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL", default="")
MAX_FILE_SIZE = os.getenv("MAX_FILE_SIZE", default=25)  # MB
