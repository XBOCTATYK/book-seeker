from typing import List

from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.analyser.models.dictionaries.WeightDictionary import WeightDictionary
from common.lib.safe_parse_to_float import safe_parse_to_float


class SummarizeGoodsService:
    _weight_dict: WeightDictionary
    _clean_data_params_dict: ClearingDictionary

    def __init__(self, weight_dict: WeightDictionary, clean_data_params_dict: ClearingDictionary):
        self._weight_dict = weight_dict
        self._clean_data_params_dict = clean_data_params_dict

    def summarize_all(self, values: List[dict]) -> List[int]:
        return list(map(lambda item: self.summarize_item(item), values))

    def summarize_item(self, item: dict) -> int:
        result = 0
        for weight in self._weight_dict.values():
            value = safe_parse_to_float(item[self._clean_data_params_dict.select_name(weight.param_name)])
            result = result + value * weight.weight_value

        return result
