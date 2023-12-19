from typing import List

from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from common.lib.make_filter import make_filter_for_map


class FilteringProcessor(AbstractProcessor):
    _filters = [
        make_filter_for_map('b_review_nr', lambda x: x > 60)
    ]

    def process(self, values: List[dict]) -> List[dict]:
        result = []

        for current_filter in self._filters:
            result = list(filter(current_filter, values))

        return result
