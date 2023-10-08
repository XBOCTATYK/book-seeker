from apps.AbstractApp import AbstractApp
from apps.scavenger.services.RawDataRepository import RawDataRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class AnalyserApp(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None
    _repository = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._repository = RawDataRepository(self._data_source)

        self._repository.get_first()


