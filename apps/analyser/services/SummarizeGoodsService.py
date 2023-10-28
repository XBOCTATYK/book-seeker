from typing import List

from apps.analyser.models.dictionaries.WeightDictionary import WeightDictionary


class SummarizeGoodsService:
    _weight_dict: WeightDictionary

    def __init__(self, weight_dict: WeightDictionary):
        self._weight_dict = weight_dict

    def summarize_all(self, values: List[dict]) -> List[int]:
        return list(map(lambda item: self.summarize_item(item), values))

    def summarize_item(self, item: dict) -> int:
        result = 0
        for weight in self._weight_dict.values():
            result = result + item[weight] * self._weight_dict.select_by_id(weight)

        return result
