import asyncio
from typing import Final

from loguru import logger
import os

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Dispatcher
from fire import Fire

TG_BOT_TOKEN: Final[str] = os.getenv("TG_BOT_TOKEN")
UPDATE_QUEUE: Final[asyncio.Queue] = asyncio.Queue()
BOT_INSTANCE: Final[Bot] = Bot(TG_BOT_TOKEN)
UPDATER: Final[Updater] = Updater(bot=BOT_INSTANCE, update_queue=UPDATE_QUEUE)
DISPATCHER: Final[Dispatcher] = Dispatcher(bot=BOT_INSTANCE, update_queue=UPDATE_QUEUE)

async def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Send me a picture and I will save it.')

async def save_photo(update, context):
    """Save photo sent by the user."""
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('pictures/photo.jpg')
    update.message.reply_text('Photo saved!')

async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


async def main():
    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.PHOTO, save_photo))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    Fire(main)