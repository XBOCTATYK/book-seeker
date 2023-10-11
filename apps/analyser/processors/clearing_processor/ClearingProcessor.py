from apps.analyser.model.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.processors.clearing_processor.ClearDataSelector import ClearDataSelector
from apps.analyser.repositories.CleanDataRepository import CleanDataRepository


class ClearingProcessor(AbstractProcessor):
    _selector: ClearDataSelector = None

    def __init__(self, selector: ClearDataSelector, repository: CleanDataRepository):
        self._selector = selector

    def process(self, dto: RawDataDecodedDto):
        result = self._selector.select_values(dto.data)



