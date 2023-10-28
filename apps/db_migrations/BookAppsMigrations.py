from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import insert

from apps.AbstractApp import AbstractApp
from apps.analyser.models.db.CleanDataDto import CleanDataDto
from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from apps.analyser.models.db.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto
from apps.analyser.models.db.ParamWeightDto import ParamWeightDto

from apps.db_migrations.dictionaries import migration_dictionaries
from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from apps.scavenger.models.db.RawFetchOptions import RawFetchOptions
from common.model.db.AppConfigDto import AppConfigDto
from common.model.db.OffsetPointerDto import OffsetPointerDto
from datasource import DbLikeDataSource
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.configs.DbConfig import DbConfig


class BookAppsMigrations(AbstractApp):
    models = []
    data_source: DbLikeDataSource
    config = None
    _entities = [
        RawOptionsDataDto,
        AppConfigDto,
        FetchOptionsTable,
        FilterOptionsTable,
        FilterTypesTable,
        OffsetPointerDto,
        CleanDataDto,
        CleanDataParamsDictionaryDto,
        CleanDataParamDto,
        ParamWeightDto,
        FilteredResultDto,
        RawFetchOptions,
    ]

    def __init__(self, data_source: DbLikeDataSource, config: DbConfig):
        super().__init__(config)

        self.data_source = data_source
        self.config = config

    def start(self):
        connection: Connection = self.data_source.get_connection()

        for dto in self._entities:
            dto.metadata.create_all(connection, checkfirst=True)

        connection.commit()

        self._insert_dictionaries(connection)

    def stop(self):
        self.data_source.close_session()

    def exports(self) -> dict:
        return {}

    def _insert_dictionaries(self, connection: Connection):
        for key in migration_dictionaries.keys():
            dict_item = migration_dictionaries[key]
            try:
                connection.begin()

                values = list(map(lambda x: {'name': x}, dict_item))
                entity = list(filter(lambda x: x.__tablename__ == key, self._entities))[0]
                clean_data_dict_statement = insert(entity).values(values)
                connection.execute(clean_data_dict_statement)

                connection.commit()
            except Exception as err:
                connection.rollback()
                raise err
