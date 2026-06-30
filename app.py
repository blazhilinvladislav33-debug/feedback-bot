import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Ваші налаштування
API_TOKEN = '8576872452:AAHjOlZkAqtRom8ADS2tO4Jx00VblJ3hN3o'
ADMIN_CHAT_ID = -1004110475608 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ОБРОБНИКИ ТЕЛЕГРАМ-БОТА ---

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != ADMIN_CHAT_ID:
        await message.answer("Вітаю! Напишіть своє повідомлення сюди, і наша команда відповість вам найближчим часом.")

@dp.message(F.chat.id == ADMIN_CHAT_ID)
async def handle_admin_reply(message: Message):
    if message.reply_to_message and message.reply_to_message.forward_origin:
        try:
            user_id = message.reply_to_message.forward_origin.sender_user.id
            await bot.send_message(chat_id=user_id, text=message.text)
        except Exception:
            await message.answer("Помилка: можливо, у користувача прихований профіль для пересилання повідомлень.")
    else:
        pass

@dp.message(F.chat.type == "private")
async def handle_user_message(message: Message):
    await bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer("Ваше повідомлення надіслано! Очікуйте на відповідь.")

# --- НЕВИДИМИЙ ПІНГАТОР (Щоб сервер не спав) ---

async def ping_handler(request):
    # Ця відповідь існує лише для сервера, в Telegram вона не потрапить
    return web.Response(text="Bot is awake and working!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', ping_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render автоматично видає порт через змінну середовища
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Фоновий вебсервер запущено на порту {port}")

async def main():
    # Одночасно запускаємо і вебсервер-пінгатор, і самого бота
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
