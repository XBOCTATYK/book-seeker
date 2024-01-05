from DateTime import DateTime

from apps.event_bus.model.Event import Event
from apps.event_bus.model.db.MessageDto import MessageDto
from common.mappers.OneDirectionMapper import OneDirectionMapper
from common.services.Decoder import Decoder


class MessageToDtoMapper(OneDirectionMapper):
    _decoder = None

    def __init__(self, decoder: Decoder):
        self._decoder = decoder

    def convert(self, message_dto: MessageDto) -> Event:
        message_data = self._decoder.decode(message_dto.text)

        return Event(
            message_dto.topic,
            message_data.type,
            message_data.data,
            DateTime(message_dto.created_at)
        )
