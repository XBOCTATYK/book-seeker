# abstract app class
from abc import ABC, abstractmethod


class AbstractApp(ABC):
    _config: dict = None
    _is_started: bool = False

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def start(self):
        self._is_started = True
        print('App started!')

    @abstractmethod
    def stop(self):
        self._is_started = False
        print('App stopped!')

    @abstractmethod
    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        pass
