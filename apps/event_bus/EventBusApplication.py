from apps.AbstractApp import AbstractApp
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class EventBusApplication(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None

    def __init__(self, config: dict):
        super().__init__(config)
        self._config = config

    def start(self):
        print('Scavenger has started!')
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    def start_migrations(self) -> AbstractMigrationScheme:
        pass



