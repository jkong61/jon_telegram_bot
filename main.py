import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import ChatActions
from aiohttp import ClientSession

URL = 'https://my-json-server.typicode.com/typicode/demo/db'
API_TOKEN = "TOKEN HERE"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def fetch(url : str, session :  ClientSession):
  async with session.get(url) as response:
    return await response.text()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
  await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler(commands=['getdata'])
async def send_welcome(message: types.Message):
  await message.answer_chat_action(ChatActions.TYPING)
  async with ClientSession() as session:
    data = await fetch(URL, session=session)
  await message.answer(data)

@dp.message_handler()
async def echo(message: types.Message):
  await message.answer(message.text)

@dp.message_handler(content_types=types.ContentTypes.STICKER)
async def handle_sticker(message: types.Message):
  if bool(message.sticker):
    await message.answer_sticker(message.sticker.file_id)
  await message.answer('Cute sticker!')

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)