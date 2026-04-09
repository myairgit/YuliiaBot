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
PRODUCTS = {
    "video_course": {
        "name": "🎥 Видео курс",
        "price": 1000,
        "type": "digital"
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

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=p["name"], callback_data=k)]
        for k, p in PRODUCTS.items()
    ])

    await message.answer("Выбери продукт 👇", reply_markup=kb)

async def reminder(user_id):
    await asyncio.sleep(3600)

    if not user_bought(user_id): # type: ignore
        await bot.send_message(
            user_id,
            "👀 Ты всё ещё не выбрал продукт"
        )
@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "video":
        link = create_payment_link(user_id, "video", 1000)
        await callback.message.answer(f"💳 Оплатить: {link}")

    elif callback.data == "chat":
        link = create_payment_link(user_id, "chat", 500)
        await callback.message.answer(f"💳 Оплатить: {link}")

        
@dp.callback_query()
async def buy(callback: types.CallbackQuery):
    product = PRODUCTS[callback.data]

    link = create_payment_link(
        user_id=callback.from_user.id,
        product=callback.data,
        amount=product["price"]
    )

    await callback.message.answer(f"💳 Оплата: {link}")


    await bot.send_message(user_id, "💬 Подписка активирована") # type: ignore


    if subscription_expired(user_id): # type: ignore
     await bot.send_message(user_id, "⛔ подписка окончена") # type: ignore


     await stripe.Subscription.delete(sub_id) # type: ignore

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
            
        if product_type == "video_course": # type: ignore
         await bot.send_video(user_id, video="FILE_ID")

    elif product_type == "event_access": # type: ignore
      await send_event_access(user_id) # type: ignore

    elif product_type == "subscription": # pyright: ignore[reportUndefinedVariable]
     await add_subscription(user_id) # type: ignore

    return {"ok": True}

# ---------------- START ----------------

async def run_bot():
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup():
    asyncio.create_task(run_bot())