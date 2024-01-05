from abc import ABC, abstractmethod
from typing import Callable, Any

PollHandler = Callable[[Any], None]


class PollManager(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def add_handler(self, handler: PollHandler):
        pass
