from abc import ABC, abstractmethod


class EventFetcher(ABC):
    _config: dict

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def fetch_events(self):
        pass
