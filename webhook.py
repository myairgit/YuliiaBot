from fastapi import FastAPI, Request # type: ignore
import stripe # type: ignore
from aiogram import Bot # type: ignore
from config import STRIPE_SECRET, BOT_TOKEN # type: ignore

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

stripe.api_key = STRIPE_SECRET

@app.post("/webhook")
async def stripe_webhook(request: Request):
    data = await request.json()

    if data["type"] == "checkout.session.completed":
        session = data["data"]["object"]

        user_id = session["metadata"]["tg_id"]
        product = session["metadata"]["product"]

        if product == "video":
            await bot.send_message(user_id, "Оплата прошла ✅")
            await bot.send_video(
                user_id,
                video="FILE_ID_ВИДЕО",
                protect_content=True
            )

        if product == "chat":
            invite = await bot.create_chat_invite_link(
                chat_id=-1001234567890,
                member_limit=1
            )

            await bot.send_message(user_id, f"Доступ: {invite.invite_link}")

    return {"ok": True}