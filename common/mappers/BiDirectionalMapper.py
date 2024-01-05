from abc import ABC, abstractmethod
from typing import TypeVar

from common.model.db.BaseDto import BaseDto

T = TypeVar('T')
K = TypeVar('K', bound=BaseDto)


class BiDirectionalMapper(ABC):
    @abstractmethod
    def to_dto(self, entity: T) -> K:
        pass

    @abstractmethod
    def to_entity(self, dto: K) -> T:
        pass
