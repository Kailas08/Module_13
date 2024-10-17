from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = ''

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Описание состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обработчик команды /start или /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать! Напишите 'Calories', чтобы начать.")


# Обработчик ввода команды 'Calories'
@dp.message_handler(Text(equals='Calories', ignore_case=True))
async def set_age(message: types.Message):
    await UserState.age.set()
    await message.reply("Введите свой возраст:")


# Обработчик возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await UserState.next()
    await message.reply("Введите свой рост (в см):")


# Обработчик роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await UserState.next()
    await message.reply("Введите свой вес (в кг):")


# Обработчик веса и расчет калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))

    # Получение сохраненных данных
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула Миффлина-Сан Жеора (упрощенная для мужчин)
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.reply(f"Ваша норма калорий: {calories} калорий в день.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)