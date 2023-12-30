from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from apps.AbstractApp import AbstractApp
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.notifier.config.NofitierConfig import NotifierConfig
from apps.notifier.db_migrations.NotifierMigrationScheme import NotifierMigrationScheme
from apps.notifier.handlers.AddTaskHandler import AddTaskHandler
from apps.notifier.handlers.StartHandlers import StartHandler
from apps.notifier.handlers.TelegramHandler import TelegramHandler
from apps.notifier.models.AppConfig import AppConfig
from apps.notifier.repositories.TgUserRepository import TgUserRepository
from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository
from apps.notifier.services.FilteredResultMessageFormatter import FilteredResultMessageFormatter
from apps.notifier.services.RawFetchOptionsService import RawFetchOptionsService
from apps.notifier.services.TgUsersNotifier import TgUsersNotifier
from apps.raw_fetch_options_processor.repositories.RawFetchOptionsRepository import RawFetchOptionsRepository
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class NotifierApp(AbstractApp):
    _config: NotifierConfig
    _handlers: List[TelegramHandler] = [
        StartHandler()
    ]
    _data_source: DbLikeDataSource
    _offset_pointer_notifier: OffsetPointerRepository
    _offset_pointer_notifier_name = 'notifier_app'
    _filtered_data_repository: FilteredDataRepository
    _tg_user_to_fetch_options_repository: TgUserToFetchOptionsRepository
    _tg_user_to_fetch_offset_pointer: OffsetPointerRepository
    _tg_user_to_fetch_offset_pointer_name = 'tg_user_to_fetch'
    _telegram_application: Application
    _scheduler: AsyncIOScheduler
    _tg_users_notifier: TgUsersNotifier
    _tg_user_repository: TgUserRepository
    _raw_fetch_options_service: RawFetchOptionsService
    _raw_fetch_options_repository: RawFetchOptionsRepository

    def __init__(self, config: NotifierConfig):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        bot_config = self._config['bot']
        web_config = self._config['web']

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
        self._raw_fetch_options_repository = RawFetchOptionsRepository(
            self._data_source, OffsetPointerRepository(self._data_source, 'raw_fetch_options_notifier')
        )
        self._raw_fetch_options_service = RawFetchOptionsService(self._raw_fetch_options_repository)
        self._tg_users_notifier = TgUsersNotifier(
            self._tg_user_to_fetch_options_repository,
            self._tg_user_repository,
            FilteredResultMessageFormatter(
                ClearingDictionary(self._data_source),
                web_config
            )
        )

        self._handlers.append(AddTaskHandler(self._raw_fetch_options_service))

        self._run_telegram_app(bot_config)

    async def _job(self, ctx):
        print('Scheduler is running!')
        bot: Bot = self._telegram_application.bot

        results = self._filtered_data_repository.process_next_n(
            10,
            lambda filtered_results: filtered_results
        )

        await self._tg_users_notifier.notify(bot, results)

    def _run_telegram_app(self, bot_config: AppConfig):
        bot_api_token = bot_config['token']
        self._telegram_application = ApplicationBuilder().token(bot_api_token).build()

        for telegram_handler in self._handlers:
            current_handler: TelegramHandler = telegram_handler
            command_handler = CommandHandler(
                current_handler.command,
                current_handler.get_handler()
            )

            self._telegram_application.add_handler(command_handler)

        self._scheduler = self._telegram_application.job_queue.scheduler
        self._telegram_application.job_queue.run_repeating(self._job, 3)

        self._telegram_application.run_polling(poll_interval=bot_config['poll_interval'])
        print('Telegram bot is running')

    def stop(self):
        self._data_source.close_session()
        self._scheduler.shutdown(wait=True)

    def exports(self) -> dict:
        return {}

    def start_migrations(self) -> NotifierMigrationScheme:
        return NotifierMigrationScheme(self._config['bot'])
