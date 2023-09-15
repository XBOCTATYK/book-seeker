import json
import os

from DateTime import DateTime

from apps.scavenger.models.logic.Coordinate import Coordinate
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox
from apps.scavenger.models.mappers.filter_options_mapper import FilterOptionsSerializer
from apps.scavenger.services.BookDataFetcher import BookDataFetcher
from apps.scavenger.services.DataFetcher import DataFetcher
from apps.scavenger.services.FilterFetcher import FilterFetcher
from apps.scavenger.services.LocalFileDataFetcher import LocalFileDataFetcher
from apps.scavenger.services.RawDataRepository import RawDataRepository
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.DbDataSource import DbDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider
from datasource.rest.UrlUtils import UrlUtils


class ScavengerApp:
    _config: dict = None
    _data_source: DbDataSource = None
    _data_fetcher: DataFetcher = None
    _url_utils: UrlUtils = UrlUtils()
    _repository: RawDataRepository = None
    _fiter_fetcher: FilterFetcher = None

    def __init__(self, config: dict):
        self._config = config

        self._data_fetcher = BookDataFetcher(self._url_utils, FilterOptionsSerializer(), config['web'], config['book'], config['secret_headers'])
        # self._data_fetcher = LocalFileDataFetcher()

    def start(self):
        print('Scavenger has started!')
        db_config = self._config['db']
        self._data_source = DbDataSource(PostgresDataProvider(db_config))
        self._repository = RawDataRepository(self._data_source)
        self._fiter_fetcher = FilterFetcher(self._data_source)
        options = self._fiter_fetcher.fetch()
        print(options)
        data = self._data_fetcher.fetch(options[0])

        print(data)

        # writes possible hotels to repository
        for item in data['b_hotels']:
            self._repository.save(
                RawOptionsDataDto(
                    raw_data=json.JSONEncoder().encode(item),
                    writer=os.getlogin(),
                    datetime=DateTime().ISO()
                )
            )
