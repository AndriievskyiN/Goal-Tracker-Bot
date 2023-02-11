from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

from hidden import TOKEN
from scraper import Scraper
from data_writer import DataWriter
from keyboards import Keyboard

# Setting up the bot
bot = Bot(token=TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot) # , storage=storage

# Initialize objects
data_writer = DataWriter()
goal_mode_keyboard = Keyboard.goal_mode_keyboard()

# START COMMAND
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer("Hello World!")

@dp.message_handler(commands=["getgoals"])
async def get_goals_mode(message: types.Message):
   await message.answer("Виберіть період за який хочете побачити інформацію", reply_markup=goal_mode_keyboard)

@dp.callback_query_handler(text=["week", "month", "year"])
async def handle_goals_mode(call: types.CallbackQuery):
    await call.message.delete()

    mode = call.data
    data_writer.TEST_get_goals_xl(mode, "total")
    doc = open("Report.xlsx", "rb")
    await bot.send_document(call.message.chat.id, document=doc)

    # Delete the document
    os.system("rm Report.xlsx")

@dp.message_handler(commands=["getmeasurements"])
async def get_measurements(message: types.Message):
    doc = open("Measurements.xlsx", "rb")
    await bot.send_document(message.chat.id, document=doc)

@dp.message_handler(lambda message: not message.text.startswith("/get"))
async def scrape(message: types.Message):
    goals = Scraper.scrape_goals(message.text)
    # measurements = Scraper.scrape_measurements(message.text)
    data_writer.write_goal_data_db(goals)
    # data_writer.write_measurement_data(measurements)

    await message.answer("✅")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)