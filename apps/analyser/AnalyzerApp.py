from typing import List

from apps.AbstractApp import AbstractApp
from apps.analyser.RecordDecoder import RecordDecoder
from apps.analyser.mappers.RawDataDecodedDtoMapper import RawDataDecodedDtoMapper
from apps.analyser.model.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.filtering_processor.FilteringProcesor import FilteringProcessor
from apps.analyser.processors.persisting_processor.PersistDataMapper import PersistDataMapper
from apps.analyser.processors.persisting_processor.PersistingProcessor import PersistingProcessor
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository
from apps.analyser.services.ClearDataSelectorService import ClearDataSelectorService
from apps.analyser.model.dictionaries.ClearingDictionary import ClearingDictionary
from apps.scavenger.services.RawDataRepository import RawDataRepository
from common.mappers.AbstractMapper import AbstractMapper
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
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
    _clear_data_selector_service: ClearDataSelectorService
    _processors: List[AbstractProcessor] = [
        FilteringProcessor()
    ]

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
        clearing_dictionary = ClearingDictionary(self._data_source)
        self._processors.append(
            PersistingProcessor(CleanDataRepository(self._data_source), PersistDataMapper(clearing_dictionary))
        )
        self._clear_data_selector_service = ClearDataSelectorService(clearing_dictionary)

        dto_list: List[RawOptionsDataDto] = self._repository.find_next_n(4)
        decoded_dto_list: List[RawDataDecodedDto] = list(map(lambda dto: self._db_raw_data_mapper.convert(dto), dto_list))
        selected_values = list(map(lambda dto: self._clear_data_selector_service.select_to_dict(dto.data), decoded_dto_list))

        result = []
        for processor in self._processors:
            result = processor.process(selected_values)

        print(result)
