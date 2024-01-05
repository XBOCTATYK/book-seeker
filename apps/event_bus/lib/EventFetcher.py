from abc import ABC, abstractmethod

from apps.event_bus.model.Event import Event


class EventFetcher(ABC):
    _config: dict

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def fetch_events(self) -> list[Event]:
        pass
