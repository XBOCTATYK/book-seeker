from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')


class MessageFormatter(ABC):
    @abstractmethod
    def format(self, value: T) -> str:
        pass
