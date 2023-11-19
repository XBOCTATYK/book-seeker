from apscheduler.schedulers.blocking import BlockingScheduler

from apps.AbstractApp import AbstractApp
from apps.raw_fetch_options_processor.db_migrations.RawFetchOptionsProcessorAppMigrationsScheme import \
    RawFetchOptionsProcessorAppMigrationsScheme
from apps.raw_fetch_options_processor.mappers.FetchOptionsDeserializer import FetchOptionsDeserializer
from apps.raw_fetch_options_processor.repositories.RawFetchOptionsRepository import RawFetchOptionsRepository
from apps.raw_fetch_options_processor.services.DataFromUrlDecoder import DataFromUrlDecoder
from apps.scavenger.repositories.FetchOptionsRepository import FetchOptionsRepository
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class RawFetchOptionsProcessorApp(AbstractApp):
    _config = None
    _data_from_url_decoder: DataFromUrlDecoder
    _raw_fetch_dara_repository: RawFetchOptionsRepository
    _fetch_options_repository: FetchOptionsRepository
    _filter_type_dictionary: FilterTypeDictionary
    _fetch_options_deserializer: FetchOptionsDeserializer
    _data_source = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'raw_fetch_options_app'
    _scheduler = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._scheduler = BlockingScheduler()

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._data_from_url_decoder = DataFromUrlDecoder()
        self._analyser_offset_repository = OffsetPointerRepository(
            self._data_source,
            self._analyser_offset_repository_name
        )
        self._raw_fetch_dara_repository = RawFetchOptionsRepository(self._data_source, self._analyser_offset_repository)
        self._filter_type_dictionary = FilterTypeDictionary(self._data_source)
        self._fetch_options_repository = FetchOptionsRepository(self._data_source, self._filter_type_dictionary)
        self._fetch_options_deserializer = FetchOptionsDeserializer()
        self._job()

    def _job(self):
        self._raw_fetch_dara_repository.process_next_n_records(
            10,
            lambda records: self._fetch_options_repository.insert_values(
                list(map(lambda rec: self._decode_data_to_dict(rec.url), records))
            )
        )

    def _decode_data_to_dict(self, url: str) -> dict:
        decoded = self._data_from_url_decoder.decode(url)
        return self._fetch_options_deserializer.deserialize(decoded)

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        return RawFetchOptionsProcessorAppMigrationsScheme
