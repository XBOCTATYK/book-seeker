from typing import List

from apps.analyser.processors.AbstractProcessor import AbstractProcessor


class FilteringProcessor(AbstractProcessor):
    _filters = [
        lambda x: x['b_review_nr'] > 60
    ]

    def process(self, values: List[dict]):
        result = []

        for current_filter in self._filters:
            result = list(filter(current_filter, values))

        return result
