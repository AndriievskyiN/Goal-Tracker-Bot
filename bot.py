from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

from hidden import TOKEN
from scraper import Scraper
from data_writer import DataWriter
from keyboards import Keyboard
from dialogs import GoalPreferenceParser

# Setting up the bot
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Initialize objects
data_writer = DataWriter()
goal_mode_keyboard = Keyboard.goal_mode_keyboard()
goal_sort_by_keyboard = Keyboard.goal_sort_by_keyboard()

# START COMMAND
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer("Hello World!")

@dp.message_handler(commands=["getgoals"])
async def get_goals_mode(message: types.Message):
   await message.answer("Виберіть період за який хочете побачити інформацію", reply_markup=goal_mode_keyboard)

@dp.callback_query_handler(text=["week", "month", "year"])
async def handle_goals_mode(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    mode = call.data
    await state.update_data(
        {"mode": mode}
    )

    await GoalPreferenceParser.mode.set()
    await call.message.answer("Сортувати за", reply_markup=goal_sort_by_keyboard)


@dp.callback_query_handler(state=GoalPreferenceParser.mode)
async def handle_goals_sort_by(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    mode = data["mode"]
    sort_by = call.data

    data_writer.get_goals_xl(mode, sort_by)
    doc = open("Report.xlsx", "rb")
    await bot.send_document(call.message.chat.id, document=doc)

    # Delete the document
    os.system("rm Report.xlsx")

    await state.finish()

# @dp.message_handler(commands=["getmeasurements"])
# async def get_measurements(message: types.Message):
#     doc = open("Measurements.xlsx", "rb")
#     await bot.send_document(message.chat.id, document=doc)

@dp.message_handler(lambda message: not message.text.startswith("/get"))
async def scrape(message: types.Message):
    goals = Scraper.scrape_goals(message.text)
    # measurements = Scraper.scrape_measurements(message.text)
    output_message = data_writer.write_goal_data_db(goals)
    # data_writer.write_measurement_data(measurements)

    await message.answer(output_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)