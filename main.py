import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.bot_command import BotCommand
from aiogram.types.chat import ChatActions
from aiohttp import ClientSession
from dotenv import dotenv_values
from pyngrok import ngrok

ENV = dotenv_values(".env")


URL = 'https://my-json-server.typicode.com/typicode/demo/db'
API_TOKEN = ENV['API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp):
  ngrok.set_auth_token(ENV['NGROK_TOKEN'])
  public_url = ngrok.connect(8443,bind_tls=True).public_url
  await bot.set_webhook(f"{public_url}/{API_TOKEN}")
  await bot.set_my_commands(commands=[
    BotCommand('start','Start Command'),
    BotCommand('getdata','Fetch Data From Server')
  ])

async def on_shutdown(dp):
  ngrok.kill()

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
  executor.start_webhook(
    dp,
    webhook_path="/{API_TOKEN}",
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    port=8443
  )