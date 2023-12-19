from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes

from apps.notifier.handlers.TelegramHandler import TelegramHandler
from apps.notifier.services.RawFetchOptionsService import RawFetchOptionsService


class AddTaskHandler(TelegramHandler):
    command = 'addtask'
    _raw_fetch_options_service: RawFetchOptionsService = None

    def __init__(self, raw_fetch_options_service: RawFetchOptionsService):
        super().__init__()
        self._raw_fetch_options_service = raw_fetch_options_service

    def get_handler(self):
        return lambda update, context: add_task_handler(update, context, self._save_options)

    def _save_options(self, update):
        message_text = update.message.text
        url = message_text.split(' ')[1]

        if url is None or len(url) == 0:
            return False

        self._raw_fetch_options_service.save_raw_fetch_options(url)

        return True


async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, fn: Callable[[Update, ContextTypes.DEFAULT_TYPE], bool]):
    res = fn(update, context)

    if not res:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="There is a problem to save!"
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your new fetch options were have been saved!"
    )
