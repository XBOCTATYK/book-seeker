from apps.analyser.models.db.RawDataDecodedDto import RawDataDecodedDto
from common.mappers.OneDirectionMapper import OneDirectionMapper
from apps.scavenger.models.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.Decoder import Decoder


class RawDataDecodedDtoMapper(OneDirectionMapper):
    _decoder: Decoder = None

    def __init__(self, _decoder: Decoder):
        self._decoder = _decoder

    def convert(self, dto: RawOptionsDataDto) -> RawDataDecodedDto:
        decoded_dictionary = self._decoder.decode(dto.raw_data)
        return RawDataDecodedDto(id=dto.id, writer=dto.writer, data=decoded_dictionary, datetime=dto.datetime)
