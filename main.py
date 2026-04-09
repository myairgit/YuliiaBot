import asyncio
from fastapi import FastAPI, Request
import stripe

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from config import BOT_TOKEN, STRIPE_SECRET, CURRENT_EVENT_CHAT_ID
from payments import create_payment_link

app = FastAPI()

# ❗ FIX: проверка токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is None. Проверь .env файл")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

stripe.api_key = STRIPE_SECRET

@app.get("/")
async def root():
    return {"status": "bot is running"}

# ---------------- PRODUCTS ----------------

PRODUCTS = {
    "video_course": {
        "name": "🎥 Видео курс",
        "price": 1000,
        "type": "video"
    },
    "event_access": {
        "name": "🎟 Доступ на ивент",
        "price": 500,
        "type": "event"
    },
    "subscription": {
        "name": "💬 Подписка VIP",
        "price": 1500,
        "type": "subscription"
    }
}


# ---------------- START ----------------

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=p["name"], callback_data=k)]
        for k, p in PRODUCTS.items()
    ])

    await message.answer("Выбери продукт 👇", reply_markup=kb)


# ---------------- CALLBACK ----------------

@dp.callback_query()
async def buy(callback: types.CallbackQuery):
    product_key = callback.data
    user_id = callback.from_user.id

    if product_key not in PRODUCTS:
        return

    product = PRODUCTS[product_key]

    link = create_payment_link(
        user_id=user_id,
        product=product_key,
        amount=product["price"]
    )

    await callback.message.answer(f"💳 Оплата: {link}")


# ---------------- EVENT ACCESS ----------------

async def send_event_access(user_id: int):
    invite = await bot.create_chat_invite_link(
        chat_id=CURRENT_EVENT_CHAT_ID,
        member_limit=1
    )

    await bot.send_message(user_id, f"🎟 Доступ: {invite.invite_link}")


# ---------------- WEBHOOK ----------------

@app.post("/webhook")
async def stripe_webhook(request: Request):
    data = await request.json()

    if data["type"] == "checkout.session.completed":
        session = data["data"]["object"]

        user_id = int(session["metadata"]["tg_id"])
        product = session["metadata"]["product"]

        await bot.send_message(user_id, "✅ Оплата прошла!")

        if product == "video_course":
            await bot.send_video(
                user_id,
                video="FILE_ID",
                protect_content=True
            )

        elif product == "event_access":
            await send_event_access(user_id)

        elif product == "subscription":
            await bot.send_message(user_id, "💬 Подписка активирована")

    return {"ok": True}


# ---------------- RUN BOT ----------------

async def run_bot():
    await dp.start_polling(bot)


@app.on_event("startup")
async def startup():
    asyncio.create_task(run_bot())