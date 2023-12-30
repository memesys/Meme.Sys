import asyncio
import os
from io import BytesIO
from typing import Final

from fire import Fire
from loguru import logger
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, PicklePersistence

from gpt_api import chat_gpt_description

TG_BOT_TOKEN: Final[str] = os.getenv("TG_BOT_TOKEN")
UPDATE_QUEUE: Final[asyncio.Queue] = asyncio.Queue()
# JOB_QUEUE: Final[asyncio.Queue] = asyncio.Queue()
BOT_INSTANCE: Final[Bot] = Bot(TG_BOT_TOKEN)
PERSISTENCE: Final[PicklePersistence] = PicklePersistence(filepath="bot_persistence.pkl")
UPDATER: Final[Updater] = Updater(bot=BOT_INSTANCE, update_queue=UPDATE_QUEUE)
APPLICATION: Final[Application] = (
    Application
    .builder()
    .updater(UPDATER)
    .build()
)


async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! Send me a picture and I will save it.')


async def process_photo(
        update: Update,
        context,
):
    """Save photo sent by the user."""
    photo_file = await update.message.photo[-1].get_file()
    io = BytesIO()
    await photo_file.download_to_memory(io)
    text = await chat_gpt_description(io)
    await update.message.reply_text(text)


async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    # Register handlers
    APPLICATION.add_handler(CommandHandler("start", start))
    APPLICATION.add_handler(MessageHandler(filters.PHOTO, process_photo))
    APPLICATION.add_error_handler(error)

    # Start the Bot
    APPLICATION.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    Fire(main)
