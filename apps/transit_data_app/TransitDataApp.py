from apps.AbstractApp import AbstractApp
from apps.transit_data_app.db_migrations.TransitDataAppMigrationScheme import TransitDataAppMigrationScheme
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
        pass

    def stop(self):
        pass

    def exports(self) -> dict[str, any]:
        return {
            'filtered_data_repository': self._filtered_data_repository
        }

    def start_migrations(self) -> TransitDataAppMigrationScheme:
        return TransitDataAppMigrationScheme()
