from abc import ABC, abstractmethod
from typing import TypeVar

from common.model.db.BaseDto import BaseDto

T = TypeVar('T')
K = TypeVar('K', bound=BaseDto)


class OneDirectionMapper(ABC):
    @abstractmethod
    def convert(self, dto: K) -> T:
        return None
