from apps.AbstractApp import AbstractApp
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class TransitDataApp(AbstractApp):
    _data_source: DbLikeDataSource = None
    _transit_data_offset_repository: OffsetPointerRepository = None
    _filtered_data_repository: FilteredDataRepository = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._transit_data_offset_repository = OffsetPointerRepository(self._data_source, 'transit_data_app')
        self._filtered_data_repository = FilteredDataRepository(self._data_source, self._transit_data_offset_repository)

    def start(self):
        self._filtered_data_repository.process_next_n(10, self._process)

    def _process(self, data):
        print(data)


