import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_SECRET = os.getenv("STRIPE_SECRET")
DOMAIN = os.getenv("DOMAIN")

CURRENT_EVENT_CHAT_ID = int(os.getenv("CURRENT_EVENT_CHAT_ID", "-1001234567890"))