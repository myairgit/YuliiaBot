import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_SECRET = os.getenv("STRIPE_SECRET")
DOMAIN = os.getenv("DOMAIN")