from typing import List

from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.persisting_processor.PersistDataMapper import PersistDataMapper
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository


class PersistingProcessor(AbstractProcessor):
    _repository: CleanDataRepository = None
    _mapper: PersistDataMapper

    def __init__(self, repository: CleanDataRepository, mapper: PersistDataMapper):
        self._repository = repository
        self._mapper = mapper

    def process(self, values: List[dict]):
        for item in values:
            values_to_insert = self._mapper.to_insert_list(item)
            self._repository.insert_clear_data(values_to_insert)

        return values

