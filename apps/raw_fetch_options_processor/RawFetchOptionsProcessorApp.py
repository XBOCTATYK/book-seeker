from apps.AbstractApp import AbstractApp
from apps.raw_fetch_options_processor.db_migrations.RawFetchOptionsProcessorAppMigrationsScheme import \
    RawFetchOptionsProcessorAppMigrationsScheme
from apps.raw_fetch_options_processor.repositories.RawFetchOptionsRepository import RawFetchOptionsRepository
from apps.raw_fetch_options_processor.services.DataFromUrlDecoder import DataFromUrlDecoder
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class RawFetchOptionsProcessorApp(AbstractApp):
    _config = None
    _data_from_url_decoder: DataFromUrlDecoder
    _raw_fetch_dara_repository: RawFetchOptionsRepository
    _data_source = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'raw_fetch_options_app'

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._data_from_url_decoder = DataFromUrlDecoder()
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source, self._analyser_offset_repository_name)
        self._raw_fetch_dara_repository = RawFetchOptionsRepository(self._data_source, self._analyser_offset_repository)

        self._raw_fetch_dara_repository.process_next_n_records(
            10,
            lambda records: list(map(lambda rec: self._data_from_url_decoder.decode(rec.url), records))
        )

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        return RawFetchOptionsProcessorAppMigrationsScheme
