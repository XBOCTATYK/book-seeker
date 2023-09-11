from sqlalchemy import Connection

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from common.model.db.AppConfigDto import AppConfigDto
from datasource import DbDataSource
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.configs.DbConfig import DbConfig


class BookAppsMigrations:
    models = []
    data_source: DbDataSource
    config = None

    def __init__(self, data_source: DbDataSource, config: DbConfig):
        self.data_source = data_source
        self.config = config

    def start(self):
        connection: Connection = self.data_source.get_connection()

        print(RawOptionsDataDto.metadata)
        RawOptionsDataDto.metadata.create_all(connection, checkfirst=True)
        AppConfigDto.metadata.create_all(connection, checkfirst=True)
        FetchOptionsTable.metadata.create_all(connection, checkfirst=True)
        FilterOptionsTable.metadata.create_all(connection, checkfirst=True)
        FilterTypesTable.metadata.create_all(connection, checkfirst=True)
        connection.commit()
