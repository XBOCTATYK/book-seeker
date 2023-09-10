import json
import os

from DateTime import DateTime

from apps.scavenger.models.logic.Coordinate import Coordinate
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox
from apps.scavenger.services.BookDataFetcher import BookDataFetcher
from apps.scavenger.services.DataFetcher import DataFetcher
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

    def __init__(self, config: dict):
        self._config = config
        # self._data_fetcher = BookDataFetcher(self._url_utils, config['web'], config['book'], config['secret_headers'])
        self._data_fetcher = LocalFileDataFetcher()

    def start(self):
        print('Scavenger has started!')
        db_config = self._config['db']
        self._data_source = DbDataSource(PostgresDataProvider(db_config))
        self._repository = RawDataRepository(self._data_source)
        data = self._data_fetcher.fetch(
            FetchOptions(
                map_box=MapViewBox(
                    Coordinate(13.68641832626463, 100.42547080801124),
                    Coordinate(13.759126242275268, 100.76261375234718)
                ),
                currency='RUB',
                checkin=DateTime('2023/10/03 UTC'),
                checkout=DateTime('2023/11/03 UTC'),
                filter=FilterOptions(
                    rooms=1,
                    review_score=8,
                    oos='1',
                    min_price=1000,
                    max_price=4000,
                    currency='RUB'
                )
            )
        )

        # writes possible hotels to repository
        for item in data['b_hotels']:
            self._repository.save(
                RawOptionsDataDto(
                    raw_data=json.JSONEncoder().encode(item),
                    writer=os.getlogin(),
                    datetime=DateTime().ISO()
                )
            )
