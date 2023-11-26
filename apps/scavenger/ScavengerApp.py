import json
import os
import time

from DateTime import DateTime
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from apps.AbstractApp import AbstractApp
from apps.scavenger.db_migrations.ScavengetAppMigrationsScheme import ScavengerAppMigrationsScheme
from apps.scavenger.models.mappers.filter_options_mapper import FilterOptionsSerializer
from apps.scavenger.services.BookDataFetcher import BookDataFetcher
from apps.scavenger.services.DataFetcher import DataFetcher
from apps.scavenger.services.FilterFetcher import FilterFetcher
from apps.scavenger.repositories.RawDataRepository import RawDataRepository
from apps.scavenger.models.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider
from datasource.rest.UrlUtils import UrlUtils


class ScavengerApp(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None
    _data_fetcher: DataFetcher = None
    _url_utils: UrlUtils = UrlUtils()
    _repository: RawDataRepository = None
    _fiter_fetcher: FilterFetcher = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'scavenge_app'
    _scheduler = None
    _offset_reset_scheduler = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._data_fetcher = BookDataFetcher(
            self._url_utils,
            FilterOptionsSerializer(),
            config['web'],
            config['book'],
            config['secret_headers']
        )
        self._scheduler = BackgroundScheduler()
        self._offset_reset_scheduler = BackgroundScheduler()

    def start(self):
        print('Scavenger has started!')
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source, self._analyser_offset_repository_name)
        self._repository = RawDataRepository(DbLikeDataSource(PostgresDataProvider(db_config)), self._analyser_offset_repository)
        self._fiter_fetcher = FilterFetcher(self._data_source, self._analyser_offset_repository)

        self._scavenger_reset()
        self._run_schedulers()

    def _job(self):
        options = self._fiter_fetcher.fetch()

        if options is None:
            return

        data = self._data_fetcher.fetch(options)

        # writes possible hotels to repository
        items = list(map(lambda item: RawOptionsDataDto(
            raw_data=json.JSONEncoder().encode(item),
            writer=os.getlogin(),
            datetime=DateTime().ISO()
        ), data['b_hotels']))

        self._repository.save_all(items)

    def _scavenger_reset(self):
        min_value = self._fiter_fetcher.find_first()
        self._analyser_offset_repository.update_value(min_value)

    def _run_schedulers(self):
        self._scheduler.add_job(self._job, 'interval', minutes=1)
        self._offset_reset_scheduler.add_job(self._scavenger_reset, 'interval', hours=24)
        self._scheduler.start()
        self._offset_reset_scheduler.start()

        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()
            self._offset_reset_scheduler.shutdown()

    def stop(self):
        self._data_source.close_session()

    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        return ScavengerAppMigrationsScheme
