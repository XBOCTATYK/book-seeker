from apps.AbstractApp import AbstractApp
from apps.analyser.RecordDecoder import RecordDecoder
from apps.scavenger.services.RawDataRepository import RawDataRepository
from common.services.Decoder import Decoder
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class AnalyzerApp(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'analyzer'
    _repository = None
    _decoder: Decoder = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._decoder = RecordDecoder()

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source, self._analyser_offset_repository_name)
        self._repository = RawDataRepository(self._data_source, self._analyser_offset_repository)

        dto = self._repository.find_next()
        decoded_dictionary = self._decoder.decode(dto.raw_data)







