# abstract
from abc import ABC, abstractmethod


class ConfigFormatter(ABC):
    config = {}

    @abstractmethod
    def get_config(self) -> dict:
        raise NotImplementedError("ConfigFormatter is abstract!")
