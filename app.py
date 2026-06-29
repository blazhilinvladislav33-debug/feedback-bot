import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Ваші налаштування (вже додані!)
API_TOKEN = '8576872452:AAFj_JW_MDq560wkgOOdkgdSAP0RVdgq74c'
ADMIN_CHAT_ID = -1004110475608 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обробник команди /start для підписників
@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != ADMIN_CHAT_ID:
        await message.answer("Вітаю! Напишіть своє повідомлення сюди, і наша команда відповість вам найближчим часом.")

# Обробник відповідей від адміністраторів у закритому чаті
@dp.message(F.chat.id == ADMIN_CHAT_ID)
async def handle_admin_reply(message: Message):
    # Перевіряємо, чи це відповідь на переслане повідомлення
    if message.reply_to_message and message.reply_to_message.forward_origin:
        try:
            # Отримуємо ID підписника з оригінального повідомлення
            user_id = message.reply_to_message.forward_origin.sender_user.id
            # Відправляємо текст адміністратора підписнику
            await bot.send_message(chat_id=user_id, text=message.text)
        except Exception as e:
            await message.answer("Помилка: можливо, у користувача прихований профіль для пересилання повідомлень.")
    else:
        # Ігноруємо звичайне спілкування команди в чаті
        pass

# Обробник вхідних повідомлень від підписників
@dp.message(F.chat.type == "private")
async def handle_user_message(message: Message):
    # Пересилаємо повідомлення користувача в адмін-чат
    await bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer("Ваше повідомлення надіслано! Очікуйте на відповідь.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())