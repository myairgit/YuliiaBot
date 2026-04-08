import asyncio
from aiogram import Bot, Dispatcher, types # type: ignore
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup # type: ignore
from aiogram.filters import Command # type: ignore
from config import BOT_TOKEN # type: ignore
from payments import create_payment_link # type: ignore

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# СТАРТ
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 Видео курс", callback_data="buy_video")],
        [InlineKeyboardButton(text="💬 Доступ в чат", callback_data="buy_chat")],
    ])
    await message.answer("Выбери продукт:", reply_markup=kb)

# ОБРАБОТКА КНОПОК
@dp.callback_query()
async def handle(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "buy_video":
        link = create_payment_link(user_id, "video")
        await callback.message.answer(f"Оплатить: {link}")

    if callback.data == "buy_chat":
        link = create_payment_link(user_id, "chat")
        await callback.message.answer(f"Оплатить: {link}")

# НАПОМИНАНИЕ (пример)
async def reminder(user_id):
    await asyncio.sleep(3600)
    await bot.send_message(user_id, "Ты не завершил покупку 👀")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())