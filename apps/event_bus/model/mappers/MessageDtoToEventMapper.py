from DateTime import DateTime

from apps.event_bus.model.Event import Event
from apps.event_bus.model.db.MessageDto import MessageDto
from common.mappers.BiDirectionalMapper import BiDirectionalMapper
from common.services.Decoder import Decoder
from common.services.Encoder import Encoder


class MessageToDtoMapper(BiDirectionalMapper):
    _decoder = None
    _encoder = None

    def __init__(self, decoder: Decoder, encoder: Encoder):
        self._decoder = decoder
        self._encoder = encoder

    def to_entity(self, message_dto: MessageDto) -> Event:
        message_data = self._decoder.decode(message_dto.text)

        return Event(
            message_dto.topic,
            message_data.type,
            message_data.data,
            DateTime(message_dto.created_at)
        )

    def to_dto(self, entity: Event) -> MessageDto:
        return MessageDto(
            None,
            entity.topic,
            self._encoder.encode(entity.data),
        )
