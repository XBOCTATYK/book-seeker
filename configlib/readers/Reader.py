# abstract
from abc import ABC, abstractmethod


class Reader(ABC):
    read_str: str = ''

    @abstractmethod
    def read(self, config_name: str) -> str:
        raise NotImplementedError("ConfigReader is an abstract class!")
