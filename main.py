import os
import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ContentType
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("8269221122:AAEKhMgVz4z3kvW-PO7v6TzGK4J3J9nw8xA")
ADMIN_CHAT_ID = os.getenv("6205469928")  # set your Telegram ID or admin chat id

if not BOT_TOKEN:
    raise SystemExit("Set BOT_TOKEN environment variable")
if not ADMIN_CHAT_ID:
    raise SystemExit("Set ADMIN_CHAT_ID environment variable")

# Replace this with the URL where you host the web/index.html
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://example.com/web/index.html")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

shop_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Відкрити магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Вітаємо у магазині одягу!\n"
        "Натисніть кнопку нижче, щоб відкрити магазин:",
        reply_markup=shop_keyboard
    )

@dp.message(content_types=[ContentType.WEB_APP_DATA])
async def handle_webapp_data(message: Message):
    # message.web_app_data.data contains the JSON string sent from WebApp
    try:
        data_str = message.web_app_data.data
        data = json.loads(data_str)
    except Exception as e:
        await message.answer("Помилка при отриманні даних з WebApp.")
        logging.exception("Invalid web_app_data")
        return

    # Format order for admin
    total = sum(item.get('price', 0) * item.get('qty', 1) for item in data.get('cart', []))
    items_text = "\n".join([f"- {it.get('name')} x{it.get('qty', 1)} — {it.get('price')} грн" for it in data.get('cart', [])])
    order_text = (
        f"🆕 Нове замовлення\n"
        f"Ім'я: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Адреса: {data.get('address')}\n"
        f"Коментар: {data.get('comment')}\n"
        f"\n🧾 Товари:\n{items_text}\n"
        f"\n💰 Сума: {total} грн\n"
        f"From user: @{message.from_user.username or message.from_user.id}"
    )
    # Send confirmation to the user
    await message.answer("✅ Дякуємо! Ми отримали ваше замовлення та зв'яжемося з вами.")
    # Forward order to admin
    await bot.send_message(int(ADMIN_CHAT_ID), order_text)

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
