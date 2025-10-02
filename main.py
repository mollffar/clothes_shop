import logging
import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ContentType
from aiogram.filters import CommandStart

# === Налаштування бота ===
BOT_TOKEN = "6929574520:AAF8eIEjZ_a2uojRsmi5rsZUgyje2J-2c54"
ADMIN_CHAT_ID = "6205469928"   # наприклад, 6205469928

# URL сторінки магазину (потрібно замінити на свій хостинг)
WEB_APP_URL = "https://example.com/web/index.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопка відкриття магазину
shop_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Відкрити магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
])

# ✅ Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Вітаємо у магазині одягу!\n"
        "Натисніть кнопку нижче, щоб відкрити магазин:",
        reply_markup=shop_keyboard
    )

# ✅ Обробка даних з WebApp
@dp.message(content_types=[ContentType.WEB_APP_DATA])
async def handle_webapp_data(message: Message):
    try:
        data_str = message.web_app_data.data
        data = json.loads(data_str)
    except Exception:
        await message.answer("❌ Помилка при отриманні даних з WebApp.")
        logging.exception("Invalid web_app_data")
        return

    # Підрахунок суми
    total = sum(item.get('price', 0) * item.get('qty', 1) for item in data.get('cart', []))
    items_text = "\n".join([f"- {it.get('name')} x{it.get('qty', 1)} — {it.get('price')} грн" for it in data.get('cart', [])])

    # Формування повідомлення
    order_text = (
        f"🆕 Нове замовлення\n"
        f"Ім'я: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Адреса: {data.get('address')}\n"
        f"Коментар: {data.get('comment')}\n"
        f"\n🧾 Товари:\n{items_text}\n"
        f"\n💰 Сума: {total} грн\n"
        f"Від користувача: @{message.from_user.username or message.from_user.id}"
    )

    # Відповідь користувачу
    await message.answer("✅ Дякуємо! Ми отримали ваше замовлення та зв'яжемося з вами.")
    # Надсилання адміну
    await bot.send_message(int(ADMIN_CHAT_ID), order_text)

# === Запуск бота ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
