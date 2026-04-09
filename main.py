import asyncio
from fastapi import FastAPI, Request
import stripe

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from config import BOT_TOKEN, STRIPE_SECRET
from payments import create_payment_link

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

stripe.api_key = STRIPE_SECRET


@dp.message()
async def get_id(message: types.Message):
    print(message.chat.id)

# ---------------- BOT ----------------

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 Видео", callback_data="video")],
        [InlineKeyboardButton(text="💬 Чат", callback_data="chat")]
    ])
    await message.answer("Выбери продукт:", reply_markup=kb)

@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "video":
        link = create_payment_link(user_id, "video", 1000)
        await callback.message.answer(f"💳 Оплатить: {link}")

    elif callback.data == "chat":
        link = create_payment_link(user_id, "chat", 500)
        await callback.message.answer(f"💳 Оплатить: {link}")
# ---------------- WEBHOOK ----------------

@app.post("/webhook")
async def stripe_webhook(request: Request):
    data = await request.json()

    if data["type"] == "checkout.session.completed":
        session = data["data"]["object"]

        user_id = int(session["metadata"]["tg_id"])
        product = session["metadata"]["product"]

        if product == "video":
            await bot.send_message(user_id, "✅ Оплата прошла!")
            await bot.send_video(
                user_id,
                video="FILE_ID",
                protect_content=True
            )

    return {"ok": True}

# ---------------- START ----------------

async def run_bot():
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup():
    asyncio.create_task(run_bot())