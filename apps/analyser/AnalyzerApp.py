from typing import List

from apscheduler.schedulers.blocking import BlockingScheduler

from apps.AbstractApp import AbstractApp
from apps.analyser.mappers.RecordDecoder import RecordDecoder
from apps.analyser.db_migrations.AnalyserAppMigrationScheme import AnalyserAppMigrationScheme
from apps.analyser.mappers.RawDataDecodedDtoMapper import RawDataDecodedDtoMapper
from apps.analyser.models.db.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.models.dictionaries.WeightDictionary import WeightDictionary
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.filtering_processor.FilteringProcesor import FilteringProcessor
from apps.analyser.processors.persisting_processor.PersistDataMapper import PersistDataMapper
from apps.analyser.processors.persisting_processor.PersistingProcessor import PersistingProcessor
from apps.analyser.processors.top_best_processor.TopBestPickService import TopBestPickService
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository
from apps.analyser.repositories.FilteredCleanDataRepository import FilterCleanDataRepository
from apps.analyser.services.ClearDataSelectorService import ClearDataSelectorService
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.analyser.services.ProcessorRunner import ProcessorRunner
from apps.analyser.services.SummarizeGoodsService import SummarizeGoodsService
from apps.scavenger.repositories.RawDataRepository import RawDataRepository
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository
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
    _raw_data_repository = None
    _filtered_clean_data_repository = None
    _filtered_data_repository = None
    _db_raw_data_mapper: OneDirectionMapper = None
    _clear_data_selector_service: ClearDataSelectorService
    _top_best_service: TopBestPickService
    _processors: List[AbstractProcessor] = [
        FilteringProcessor()
    ]
    _processor_runner = None
    _scheduler = None

    def __init__(self, config: dict):
        super().__init__(config)

        self._config = config
        self._db_raw_data_mapper = RawDataDecodedDtoMapper(RecordDecoder())
        self._processor_runner = ProcessorRunner(self._processors)
        self._scheduler = BlockingScheduler()

    def start(self):
        db_config = self._config['db']
        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._analyser_offset_repository = OffsetPointerRepository(self._data_source,
                                                                   self._analyser_offset_repository_name)
        self._raw_data_repository = RawDataRepository(self._data_source, self._analyser_offset_repository)
        clearing_dictionary = ClearingDictionary(self._data_source)
        self._processors.append(
            PersistingProcessor(
                CleanDataRepository(self._data_source),
                PersistDataMapper(clearing_dictionary)
            )
        )
        self._filtered_clean_data_repository = FilterCleanDataRepository(
            self._data_source,
            OffsetPointerRepository(self._data_source, 'filter_clean_data')
        )
        self._filtered_data_repository = FilteredDataRepository(
            self._data_source,
            OffsetPointerRepository(self._data_source, 'filtered_data')
        )
        self._clear_data_selector_service = ClearDataSelectorService(clearing_dictionary)
        self._top_best_service = TopBestPickService(
            SummarizeGoodsService(
                WeightDictionary(self._data_source),
                clearing_dictionary,
            ),
            self._filtered_data_repository
        )

        self._run_schedulers()

    def stop(self):
        self._data_source.close_session()
        self._scheduler.shutdown(wait=True)

    def _job(self):
        print('Cleaning raw data!')
        self._raw_data_repository.process_next_n(10, self._process_data)

        print('Filtering data')
        self._filtered_clean_data_repository.process_n_records(
            100,
            lambda record_list: self._top_best_service.pick_and_save_top_options(
                record_list,
                self._config['analyser']['pick_top']
            )
        )

    def _run_schedulers(self):
        self._scheduler.add_job(self._job, 'interval', seconds=5)
        self._scheduler.start()

    def exports(self) -> dict:
        return {}

    def _process_data(self, dto_list: list[RawOptionsDataDto]):
        decoded_dto_list: List[RawDataDecodedDto] = list(map(
            lambda dto: self._db_raw_data_mapper.convert(dto),
            dto_list
        ))
        selected_values: List[dict[str, str]] = list(map(
            lambda dto: self._clear_data_selector_service.select_to_dict(dto.data),
            decoded_dto_list
        ))

        result = self._processor_runner.process(selected_values)
        return result

    def start_migrations(self) -> AnalyserAppMigrationScheme:
        return AnalyserAppMigrationScheme()
