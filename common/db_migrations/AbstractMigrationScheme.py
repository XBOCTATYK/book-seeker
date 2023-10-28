from abc import ABC, abstractmethod
from typing import List, Type, Callable

from sqlalchemy import Connection

from common.model.db.BaseDto import BaseDto


class AbstractMigrationScheme(ABC):
    @abstractmethod
    def get_tables(self) -> List[Type[BaseDto]]:
        return list()

    @abstractmethod
    def get_dictionaries(self) -> dict[str, List[str]]:
        return {'example': []}

    @abstractmethod
    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass

