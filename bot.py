from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

from hidden import TOKEN
from scraper import Scraper
from data_writer import DataWriter
from keyboards import Keyboard
from dialogs import GoalPreferenceParser, ReportCombiner

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


@dp.message_handler(commands=["addbyparts"])
async def addreport(message: types.Message):
    await message.answer("Відправте першу частину повідомлення")

@dp.message_handler()
async def concatfirst(message: types.Message, state: FSMContext):
    if message.text.lower().strip() == "стоп":
        state.finish()
        await message.answer("👌")

    else:
        first_part = message.text
        await state.update_data(
            {"message1": first_part}
        )

        await message.answer("Відправте другу частину повідомлення")
        await ReportCombiner.message1.set()

@dp.message_handler(state=ReportCombiner.message1)
async def concatsecond(message: types.Message, state: FSMContext):
    if message.text.lower().strip() == "стоп":
        data = await state.get_data()
        txt_report = data["message1"]

    else:
        second_part = message.text
        await state.update_data(
            {"message2": second_part}
        )

        data = await state.get_data()

        # Concatenate the messsages
        txt_report = data["message1"] + data["message2"]

        # Scrape and write data
        goals = Scraper.scrape_goals(txt_report)
        data_writer.write_goal_data_db(goals) 

    await message.answer("✅")
    await state.finish()

# @dp.message_handler(commands=["getmeasurements"])
# async def get_measurements(message: types.Message):
#     doc = open("Measurements.xlsx", "rb")
#     await bot.send_document(message.chat.id, document=doc)

@dp.message_handler(lambda message: not message.text.startswith("/get"))
async def scrape(message: types.Message):
    goals = Scraper.scrape_goals(message.text)
    # measurements = Scraper.scrape_measurements(message.text)
    data_writer.write_goal_data_db(goals)
    # data_writer.write_measurement_data(measurements)

    await message.answer("✅")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)