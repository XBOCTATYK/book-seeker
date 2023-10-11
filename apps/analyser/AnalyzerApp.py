from typing import List

from apps.AbstractApp import AbstractApp
from apps.analyser.RecordDecoder import RecordDecoder
from apps.analyser.mappers.RawDataDecodedDtoMapper import RawDataDecodedDtoMapper
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.clearing_processor.ClearDataSelector import ClearDataSelector
from apps.analyser.processors.clearing_processor.ClearingDictionary import ClearingDictionary
from apps.analyser.processors.clearing_processor.ClearingProcessor import ClearingProcessor
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository
from apps.scavenger.services.RawDataRepository import RawDataRepository
from common.mappers.AbstractMapper import AbstractMapper
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class AnalyzerApp(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'analyzer'
    _repository = None
    _db_raw_data_mapper: AbstractMapper = None
    _processors: List[AbstractProcessor] = []

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._db_raw_data_mapper = RawDataDecodedDtoMapper(RecordDecoder())

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source,
                                                                   self._analyser_offset_repository_name)
        self._repository = RawDataRepository(self._data_source, self._analyser_offset_repository)
        self._processors.append(ClearingProcessor(ClearDataSelector(
            ClearingDictionary(self._data_source)),
            CleanDataRepository(self._data_source)
        ))

        dto = self._db_raw_data_mapper.convert(self._repository.find_next())

        for processor in self._processors:
            processor.process(dto)
