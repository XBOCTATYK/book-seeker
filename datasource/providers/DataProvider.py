from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy.orm import Session

ENGINE = TypeVar('ENGINE')
CON = TypeVar('CON')
SESS = TypeVar('SESS')


class DataProvider(ABC):
    name = 'abstract'

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def connect(self) -> SESS:
        return None

    @abstractmethod
    def disconnect(self):
        return None

    @abstractmethod
    def get_connection(self) -> CON:
        return None

    @abstractmethod
    def get_engine(self) -> ENGINE:
        return None

    @abstractmethod
    def get_connect_url(self) -> str:
        return ''

    @abstractmethod
    def create_session(self) -> SESS:
        return None
