from abc import ABC, abstractmethod
from typing import TypeVar

from common.model.db.BaseDto import BaseDto

T = TypeVar('T')


class BiDirectionalMapper(ABC):
    @abstractmethod
    def to_dto(self, entity: T) -> BaseDto:
        pass

    @abstractmethod
    def to_entity(self, dto: BaseDto) -> T:
        pass
