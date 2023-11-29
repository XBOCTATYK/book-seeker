from typing import List, Type

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from apps.AbstractApp import AbstractApp
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.notifier.db_migrations.NotifierMigrationScheme import NotifierMigrationScheme
from apps.notifier.handlers.TelegramHandler import TelegramHandler
from apps.notifier.handlers.StartHandlers import StartHandler
from apps.notifier.models.AppConfig import AppConfig
from apps.notifier.repositories.TgUserRepository import TgUserRepository
from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository
from apps.notifier.services.TgUsersNotifier import TgUsersNotifier
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


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
    _tg_user_repository: TgUserRepository

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        bot_config = self._config['bot']

        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config), 'notifier_app_data_source')
        self._offset_pointer_notifier = OffsetPointerRepository(self._data_source, self._offset_pointer_notifier_name)
        self._filtered_data_repository = FilteredDataRepository(self._data_source, self._offset_pointer_notifier)
        self._tg_user_to_fetch_offset_pointer = OffsetPointerRepository(
            self._data_source,
            self._tg_user_to_fetch_offset_pointer_name
        )
        self._tg_user_repository = TgUserRepository(self._data_source)
        self._tg_user_to_fetch_options_repository = TgUserToFetchOptionsRepository(
            self._data_source,
            self._tg_user_to_fetch_offset_pointer
        )
        self._tg_users_notifier = TgUsersNotifier(
            self._tg_user_to_fetch_options_repository,
            self._tg_user_repository,
            ClearingDictionary(self._data_source)
        )

        self._scheduler = BackgroundScheduler()
        self._run_schedulers()
        self._run_telegram_app(bot_config)

    def _job(self):
        print('Scheduler is running!')
        bot: Bot = self._telegram_application.bot

        self._filtered_data_repository.process_next_n(
            10,
            lambda filtered_results: self._tg_users_notifier.notify(bot, filtered_results)
        )

    def _run_telegram_app(self, bot_config: AppConfig):
        bot_api_token = bot_config['token']
        self._telegram_application = ApplicationBuilder().token(bot_api_token).build()

        for telegram_handler in self._handlers:
            current_handler: TelegramHandler = telegram_handler()
            command_handler = CommandHandler(
                current_handler.command,
                current_handler.get_handler()
            )

            self._telegram_application.add_handler(command_handler)

        self._telegram_application.run_polling(poll_interval=bot_config['poll_interval'])
        print('Telegram bot is running')

    def _run_schedulers(self):
        self._scheduler.add_job(self._job, 'interval', seconds=10)
        self._scheduler.start()

    def stop(self):
        self._data_source.close_session()
        self._scheduler.shutdown(wait=True)

    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        return NotifierMigrationScheme
