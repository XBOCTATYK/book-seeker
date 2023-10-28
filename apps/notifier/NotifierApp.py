from typing import List

from telegram.ext import ApplicationBuilder, CommandHandler

from apps.AbstractApp import AbstractApp
from apps.notifier.handlers import TelegramHandler
from apps.notifier.handlers.StartHandlers import StartHandler


class NotifierApp(AbstractApp):
    _handlers: List[TelegramHandler] = [
        StartHandler
    ]

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        bot_config = self._config['bot']

        application = ApplicationBuilder().token(bot_config['token']).build()

        for telegram_handler in self._handlers:
            current_handler: TelegramHandler = telegram_handler()
            command_handler = CommandHandler(
                current_handler.command,
                current_handler.get_handler()
            )

            application.add_handler(command_handler)

        application.run_polling(poll_interval=2000)

    def stop(self):
        pass

    def exports(self) -> dict:
        pass
