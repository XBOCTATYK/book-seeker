from apps.analyser.model.RawDataDecodedDto import RawDataDecodedDto
from apps.analyser.processors.AbstractProcessor import AbstractProcessor


class FilteringProcessor(AbstractProcessor):
    def process(self, dto: RawDataDecodedDto):
        return None

