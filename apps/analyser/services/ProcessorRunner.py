from typing import List

from apps.analyser.processors.AbstractProcessor import AbstractProcessor


class ProcessorRunner:
    _processors: List[AbstractProcessor] = []

    def __init__(self, processors: List[AbstractProcessor]):
        self._processors = processors

    def process(self, values: List[dict[str, str]]) -> List[dict[str, str]]:
        result = []
        for processor in self._processors:
            result = processor.process(values)

        return result

