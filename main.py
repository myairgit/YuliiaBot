import asyncio
from fastapi import FastAPI, Request
import stripe

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from config import BOT_TOKEN, STRIPE_SECRET

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

stripe.api_key = STRIPE_SECRET

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
    await callback.message.answer("Оплата пока через webhook")

# ---------------- WEBHOOK ----------------

@app.post("/webhook")
async def stripe_webhook(request: Request):
    data = await request.json()

    if data["type"] == "checkout.session.completed":
        session = data["data"]["object"]

        user_id = session["metadata"]["tg_id"]

        await bot.send_message(user_id, "Оплата прошла ✅")

    return {"ok": True}


# ---------------- START ----------------

async def run_bot():
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup():
    asyncio.create_task(run_bot())