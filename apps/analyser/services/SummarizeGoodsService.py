from typing import Union

from apps.analyser.models.CleanDataEstimations import CleanDataEstimationResult
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.analyser.models.dictionaries.WeightDictionary import WeightDictionary
from common.lib.safe_parse_to_float import safe_parse_to_float


class SummarizeGoodsService:
    _weight_dict: WeightDictionary
    _clean_data_params_dict: ClearingDictionary

    def __init__(self, weight_dict: WeightDictionary, clean_data_params_dict: ClearingDictionary):
        self._weight_dict = weight_dict
        self._clean_data_params_dict = clean_data_params_dict

    def summarize(self, item: dict[int, str]) -> CleanDataEstimationResult:
        return CleanDataEstimationResult(
            estimate=self.summarize_item(item),
            param_set=item
        )

    def summarize_item(self, item: dict[int, str]) -> Union[int, float]:
        result = 0
        for weight in self._weight_dict.values():
            value = safe_parse_to_float(item[weight.param_name]) if weight.param_name in item else 0
            result = result + value * weight.weight_value

        return result
