import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_SECRET = os.getenv("STRIPE_SECRET")
DOMAIN = os.getenv("DOMAIN")

CURRENT_EVENT_CHAT_ID = -1001234567890

async def send_event_access(user_id):
    invite = await bot.create_chat_invite_link( # type: ignore
        chat_id=CURRENT_EVENT_CHAT_ID,
        member_limit=1
    )

    await bot.send_message(user_id, f"🎟 Вот доступ: {invite.invite_link}") # type: ignore