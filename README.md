# Telegram WebApp Clothing Shop + Bot Receiver
Это минимальный проект: WebApp (статический сайт) + Telegram Bot (aiogram 3.x).

Структура:
- web/ - статические файлы WebApp (index.html, app.js, style.css)
- bot/main.py - Телеграм-бот на aiogram, принимает данные из WebApp
- requirements.txt - зависимости
- start_bot.sh - скрипт запуска (Linux)

Подготовка:
1. Зарегистрируйте бота у BotFather и получите BOT_TOKEN.
2. Задайте в файле bot/.env или в окружении:
   - BOT_TOKEN (токен бота)
   - ADMIN_CHAT_ID (ID чата где бот будет присылать заказы; это ваш Telegram ID)
3. Разместите папку web/ на HTTPS-хостинге (Vercel, Netlify, GitHub Pages с HTTPS и т.д.)
   или используйте локальный ngrok/localhost.run, чтобы получить https URL.
4. В BotFather установите *ссылку на Web App* в кнопке (мы используем InlineKeyboard с web_app=URL)
   - В коде замените WEB_APP_URL в bot/main.py на URL вашего размещённого web/index.html.

Запуск:
- Установите зависимости: `pip install -r requirements.txt`
- Запустите бота: `bash start_bot.sh` (или `python bot/main.py`)

Как работает:
- Пользователь нажимает "Відкрити магазин" -> открывается WebApp в Telegram.
- В WebApp пользователь добавляет товары в корзину, заполняет имя/телефон/адрес.
- При нажатии "Оформити замовлення" WebApp отправляет заказ через Telegram.WebApp.sendData(JSON).
- Бот получает сообщение с web_app_data и пересылает заказ администратору (ADMIN_CHAT_ID).

Важно:
- Telegram Web Apps требуют HTTPS.
- Для публичного использования настройте безопасное хранение токена и валидацию входящих данных.
