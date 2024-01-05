from apps.event_bus.model.Event import Event
from apps.event_bus.repositories.EventRepository import EventRepository
from common.mappers.BiDirectionalMapper import BiDirectionalMapper


class BaseProducerService:
    _config: dict
    _topic: str
    _event_repository: EventRepository
    _mapper = None

    def __init__(self,
                 config: dict,
                 topic: str,
                 event_repository: EventRepository,
                 mapper: BiDirectionalMapper
                 ):

        self._config = config
        self._topic = topic
        self._event_repository = event_repository
        self._mapper = mapper

    def produce(self, event: Event):
        self._event_repository.save(self._mapper.to_dto(event))
