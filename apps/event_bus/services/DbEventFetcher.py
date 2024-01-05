from apps.event_bus.lib.EventFetcher import EventFetcher
from apps.event_bus.model.Event import Event
from apps.event_bus.model.mappers.JSONDecoder import JSONDecoder
from apps.event_bus.model.mappers.MessageDtoToEventMapper import MessageToDtoMapper
from apps.event_bus.repositories.EventRepository import EventRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class DbEventFetcher(EventFetcher):
    _repository: EventRepository
    _offset_name = 'events'
    _mapper = MessageToDtoMapper(JSONDecoder())

    def __init__(self, config: dict):
        super().__init__(config)

        self._data_source = DbLikeDataSource(PostgresDataProvider(config))
        self._repository = EventRepository(
            self._data_source,
            OffsetPointerRepository(self._data_source, self._offset_name)
        )

    def fetch_events(self) -> list[Event]:
        return list(map(
            lambda message_dto: self._mapper.convert(message_dto),
            self._repository.get_next_n_new_events(100)
        ))
