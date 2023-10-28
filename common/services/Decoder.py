from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')


class Decoder(ABC):
    @abstractmethod
    def decode(self, target: str) -> T:
        pass
