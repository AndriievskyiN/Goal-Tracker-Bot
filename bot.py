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
goal_mode_keyboard = Keyboard.get_keyboard("goal_mode_keyboard")
goal_sort_by_keyboard = Keyboard.get_keyboard("goal_sort_by_keyboard")

# START COMMAND
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer("Вітаю! Для початку подивіться це відео про команди цього бота: \nhttps://youtu.be/PmgiIa0ONVU")

@dp.message_handler(commands=["getgoals"])
async def get_goals_mode(message: types.Message):
   await message.answer("Виберіть період за який хочете побачити інформацію", reply_markup=goal_mode_keyboard)

@dp.callback_query_handler(text=["week", "month", "year"])
async def handle_goals_mode(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    mode = call.data
    if mode == "year":
        await call.message.answer("На даний момент ця функція не працює, виберіть інший період", reply_markup=goal_mode_keyboard)

    else:
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

    filename = data_writer.get_goals_xl(mode, sort_by)
    doc = open(filename, "rb")
    await bot.send_document(call.message.chat.id, document=doc)

    # Delete the document
    filename = filename.replace(" ", "\ ")
    os.system(f"rm {filename}")

    await state.finish()


@dp.message_handler(commands=["addbyparts"])
async def addreport(message: types.Message, state: FSMContext):
    await message.answer("Відправте першу частину повідомлення")
    await ReportCombiner.message1.set()

@dp.message_handler(state=ReportCombiner.message1)
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
        await ReportCombiner.next()

@dp.message_handler(state=ReportCombiner.message2)
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
    try:
        goals = Scraper.scrape_goals(txt_report)
    except:
        await message.answer("Не знайшов всю потрібну інформацію... Відправте початок чи кінець повідомлення")

    else:
        data_writer.write_goal_data_db(goals) 
        await message.answer("✅")
        await state.finish()

# @dp.message_handler(commands=["getmeasurements"])
# async def get_measurements(message: types.Message):
#     doc = open("Measurements.xlsx", "rb")
#     await bot.send_document(message.chat.id, document=doc)

@dp.message_handler(lambda message: not message.text.startswith("/get"))
async def scrape(message: types.Message):

    try:
        goals = Scraper.scrape_goals(message.text)
        # measurements = Scraper.scrape_measurements(message.text)
    except:
        await message.answer("Не знайшов всю потрібну інформацію... Якщо це тільки одна частина звіту, спробуйте команду /addbyparts або відправте повне повідомлення")
    else:
        data_writer.write_goal_data_db(goals)
        await message.answer("✅")
        # data_writer.write_measurement_data(measurements)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)