from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')


class Encoder(ABC):
    @abstractmethod
    def encode(self, target: T) -> str:
        pass
