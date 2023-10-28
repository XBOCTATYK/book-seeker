from abc import ABC, abstractmethod


class OneDirectionMapper(ABC):
    @abstractmethod
    def convert(self, dto):
        return None
