from typing import List

from apps.AbstractApp import AbstractApp
from apps.analyser.RecordDecoder import RecordDecoder
from apps.analyser.db_migrations.AnalyserAppMigrationScheme import AnalyserAppMigrationScheme
from apps.analyser.mappers.RawDataDecodedDtoMapper import RawDataDecodedDtoMapper
from apps.analyser.models.db.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.models.dictionaries.WeightDictionary import WeightDictionary
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.filtering_processor.FilteringProcesor import FilteringProcessor
from apps.analyser.processors.persisting_processor.PersistDataMapper import PersistDataMapper
from apps.analyser.processors.persisting_processor.PersistingProcessor import PersistingProcessor
from apps.analyser.processors.top_best_processor.TopBestProcessor import TopBestProcessor
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository
from apps.analyser.services.ClearDataSelectorService import ClearDataSelectorService
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.analyser.services.ProcessorRunner import ProcessorRunner
from apps.analyser.services.SummarizeGoodsService import SummarizeGoodsService
from apps.scavenger.repositories.RawDataRepository import RawDataRepository
from common.mappers.OneDirectionMapper import OneDirectionMapper
from apps.scavenger.models.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class AnalyzerApp(AbstractApp):
    _config: dict = None
    _data_source: DbLikeDataSource = None
    _analyser_offset_repository: OffsetPointerRepository = None
    _analyser_offset_repository_name = 'analyzer'
    _repository = None
    _db_raw_data_mapper: OneDirectionMapper = None
    _clear_data_selector_service: ClearDataSelectorService
    _processors: List[AbstractProcessor] = [
        FilteringProcessor()
    ]
    _processor_runner = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._db_raw_data_mapper = RawDataDecodedDtoMapper(RecordDecoder())
        self._processor_runner = ProcessorRunner(self._processors)

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source,
                                                                   self._analyser_offset_repository_name)
        self._repository = RawDataRepository(self._data_source, self._analyser_offset_repository)
        clearing_dictionary = ClearingDictionary(self._data_source)
        self._processors.append(
            PersistingProcessor(
                CleanDataRepository(self._data_source),
                PersistDataMapper(clearing_dictionary)
            )
        )
        self._clear_data_selector_service = ClearDataSelectorService(clearing_dictionary)

        result = self._repository.process_next_n(4, self._process_data)

        top_best_processor = TopBestProcessor(
            SummarizeGoodsService(WeightDictionary(self._data_source), clearing_dictionary)
        )
        print(result)

    def stop(self):
        self._data_source.close_session()

    def exports(self) -> dict:
        return {}

    def _process_data(self, dto_list: List[RawOptionsDataDto]):
        decoded_dto_list: List[RawDataDecodedDto] = list(map(lambda dto: self._db_raw_data_mapper.convert(dto), dto_list))
        selected_values: List[dict[str, str]] = list(map(
            lambda dto: self._clear_data_selector_service.select_to_dict(dto.data),
            decoded_dto_list
        ))

        result = self._processor_runner.process(selected_values)
        return result

    @staticmethod
    def migrations():
        return AnalyserAppMigrationScheme
