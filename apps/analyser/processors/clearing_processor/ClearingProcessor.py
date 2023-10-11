from apps.analyser.model.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.clearing_processor.ClearDataSelector import ClearDataSelector
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository


class ClearingProcessor(AbstractProcessor):
    _selector: ClearDataSelector = None
    _repository: CleanDataRepository = None

    def __init__(self, selector: ClearDataSelector, repository: CleanDataRepository):
        self._selector = selector
        self._repository = repository

    def process(self, dto: RawDataDecodedDto):
        selected_values = self._selector.select_values(dto.data)
        result = self._repository.insert_clear_data(selected_values)
        print(result)

        self._repository.get_all()



