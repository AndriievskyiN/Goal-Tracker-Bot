from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from hidden import TOKEN
from scraper import Scraper
from file_writer import FileWriter

# Setting up the bot
bot = Bot(token=TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot) # , storage=storage

# Initialize objects
file_writer = FileWriter()

# START COMMAND
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer("Hello World!")

@dp.message_handler(commands=["getfile"])
async def get_file(message: types.Message):
    doc = open("Report.xlsx", "rb")
    await bot.send_document(message.chat.id, document=doc)

@dp.message_handler(lambda message: not message.text.startswith("/getfile"))
async def scrape(message: types.Message):
    data = Scraper.scrape_report(message.text)
    file_writer.write_data(data)

    await message.answer("Done")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)