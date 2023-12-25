from telegram import Update
from telegram.ext import ContextTypes

from apps.notifier.handlers.TelegramHandler import TelegramHandler


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Now you can use /taskadd command to add new url to discover!")


class StartHandler(TelegramHandler):
    command: str = 'start'
    _active: bool = False

    def __init__(self):
        super().__init__()

    def get_handler(self):
        self._active = True

        return start_handler
