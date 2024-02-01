from typing import List, Type, Callable

from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import insert

from apps.AbstractApp import AbstractApp
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto
from datasource import DbLikeDataSource
from datasource.configs.DbConfig import DbConfig


class BookAppsMigrations(AbstractApp):
    def start_migrations(self) -> AbstractMigrationScheme:
        pass

    _data_source: DbLikeDataSource
    _config = None
    _migration_schemes: List[AbstractMigrationScheme] = []

    def __init__(self,
                 data_source: DbLikeDataSource,
                 config: DbConfig,
                 migration_schemes: List[AbstractMigrationScheme]):
        super().__init__(config)

        self._data_source = data_source
        self._config = config
        self._migration_schemes = migration_schemes

    def start(self):
        for scheme in self._migration_schemes:
            entities: List[Type[BaseDto]] = scheme.get_tables()

            connection: Connection = self._data_source.get_connection()

            for dto in entities:
                print(f'Creating table {dto.__tablename__}...')
                dto.metadata.create_all(connection, checkfirst=True)

            print('Inserting dictionaries...')
            dictionaries: dict[str, List[str]] = scheme.get_dictionaries()
            self._insert_dictionaries(connection, dictionaries, entities)

            filler_functions: List[Callable] = scheme.fill_with_data()

            if filler_functions is None:
                filler_functions = []

            for filler in filler_functions:
                filler(connection)

            connection.commit()

    def stop(self):
        self._data_source.close_session()

    def exports(self) -> dict:
        return {}

    def _insert_dictionaries(self, connection: Connection, dictionaries: dict[str, List[str]], entities: List[Type[BaseDto]]):
        for key in dictionaries.keys():
            dict_item = dictionaries[key]

            values = list(map(lambda x: {'name': x}, dict_item))
            entity = list(filter(lambda x: x.__tablename__ == key, entities))[0]
            clean_data_dict_statement = insert(entity).values(values).on_conflict_do_nothing()
            connection.execute(clean_data_dict_statement)
