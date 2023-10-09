from sqlalchemy import Connection

from apps.analyser.model.CleanDataDto import CleanDataDto
from apps.analyser.model.CleanDataParamDto import CleanDataParamDto
from apps.analyser.model.CleanDataParamsDictionary import CleanDataParamsDictionaryDto
from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from common.model.db.AppConfigDto import AppConfigDto
from common.model.db.OffsetPointerDto import OffsetPointerDto
from datasource import DbLikeDataSource
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.configs.DbConfig import DbConfig


class BookAppsMigrations:
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
    ]

    def __init__(self, data_source: DbLikeDataSource, config: DbConfig):
        self.data_source = data_source
        self.config = config

    def start(self):
        connection: Connection = self.data_source.get_connection()

        for dto in self._entities:
            dto.metadata.create_all(connection, checkfirst=True)

        connection.commit()
