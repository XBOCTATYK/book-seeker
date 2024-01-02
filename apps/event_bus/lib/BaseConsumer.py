from abc import ABC, abstractmethod


class BaseConsumer(ABC):
    _config: dict

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def on_event(self):
        pass

    def _poll_event(self):
        pass
