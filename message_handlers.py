from utils import fetch
from aiogram.types.chat import ChatActions
from aiogram import types
from aiohttp import ClientSession

URL = "https://my-json-server.typicode.com/typicode/demo/db"


async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\n")


async def get_data(message: types.Message):
    await message.answer_chat_action(ChatActions.TYPING)
    async with ClientSession() as session:
        data = await fetch(URL, session=session)
    await message.answer(data)


async def echo(message: types.Message):
    await message.answer(message.text)


async def handle_sticker(message: types.Message):
    if bool(message.sticker):
        await message.answer_sticker(message.sticker.file_id)
    await message.answer("Cute sticker!")
