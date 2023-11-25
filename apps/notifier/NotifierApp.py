from typing import List, Type

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from apps.AbstractApp import AbstractApp
from apps.notifier.handlers.TelegramHandler import TelegramHandler
from apps.notifier.handlers.StartHandlers import StartHandler
from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository
from apps.notifier.services.TgUsersNotifier import TgUsersNotifier
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class NotifierApp(AbstractApp):
    _handlers: List[Type[TelegramHandler]] = [
        StartHandler
    ]
    _data_source: DbLikeDataSource
    _offset_pointer_notifier: OffsetPointerRepository
    _offset_pointer_notifier_name = 'notifier_app'
    _filtered_data_repository: FilteredDataRepository
    _tg_user_to_fetch_options_repository: TgUserToFetchOptionsRepository
    _tg_user_to_fetch_offset_pointer: OffsetPointerRepository
    _tg_user_to_fetch_offset_pointer_name = 'tg_user_to_fetch'
    _telegram_application: Application
    _scheduler: BackgroundScheduler
    _tg_users_notifier: TgUsersNotifier

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        bot_config = self._config['bot']

        self._data_source = DbLikeDataSource(db_config, 'notifier_app_data_source')
        self._offset_pointer_notifier = OffsetPointerRepository(self._data_source, self._offset_pointer_notifier_name)
        self._filtered_data_repository = FilteredDataRepository(self._data_source, self._offset_pointer_notifier)
        self._tg_user_to_fetch_offset_pointer = OffsetPointerRepository(
            self._data_source,
            self._tg_user_to_fetch_offset_pointer_name
        )
        self._tg_user_to_fetch_options_repository = TgUserToFetchOptionsRepository(
            self._data_source,
            self._tg_user_to_fetch_offset_pointer
        )
        self._tg_users_notifier = TgUsersNotifier(self._tg_user_to_fetch_options_repository)

        self._telegram_application = ApplicationBuilder().token(bot_config['token']).build()

        for telegram_handler in self._handlers:
            current_handler: TelegramHandler = telegram_handler()
            command_handler = CommandHandler(
                current_handler.command,
                current_handler.get_handler()
            )

            self._telegram_application.add_handler(command_handler)

        self._telegram_application.run_polling(poll_interval=2000)

        self._scheduler = BackgroundScheduler()

    def _job(self):
        bot: Bot = self._telegram_application.bot

        self._filtered_data_repository.process_next_n(
            10,
            lambda chat_id, message: self._tg_users_notifier.notify(bot)
        )

    def _run_schedulers(self):
        self._scheduler.add_job(self._job)
        self._scheduler.start()

    def stop(self):
        pass

    def exports(self) -> dict:
        pass
