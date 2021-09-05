import logging
import message_handlers as handlers
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.bot_command import BotCommand
from dotenv import dotenv_values
from pyngrok import ngrok

ENV = dotenv_values(".env")
API_TOKEN = ENV["API_TOKEN"]

logging.basicConfig(level=logging.INFO)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handlers.send_welcome, commands=["start", "help"])
    dp.register_message_handler(handlers.get_data, commands=["getdata"])
    dp.register_message_handler(handlers.echo, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        handlers.handle_sticker, content_types=types.ContentTypes.STICKER
    )


async def on_startup(dp: Dispatcher):
    """
    Called during application start up
    """
    ngrok.set_auth_token(ENV["NGROK_TOKEN"])
    public_url = ngrok.connect(8443, bind_tls=True).public_url
    bot = dp.bot

    await bot.set_webhook(f"{public_url}/{API_TOKEN}")
    await bot.set_my_commands(
        commands=[
            BotCommand("start", "Start Command"),
            BotCommand("getdata", "Fetch Data From Server"),
        ]
    )
    register_handlers(dp)


async def on_shutdown(dp: Dispatcher):
    """
    Called during application shut down
    """
    ngrok.kill()


if __name__ == "__main__":
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    executor.start_webhook(
        dp,
        webhook_path="/{API_TOKEN}",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        port=8443,
    )
