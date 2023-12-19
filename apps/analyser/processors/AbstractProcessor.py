from abc import ABC, abstractmethod
from typing import List


class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, values: List[dict]) -> List[dict]:
        return []
