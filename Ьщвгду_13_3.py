from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий Вашему здоровью")

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start чтобы начать наше общение")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)