from functools import reduce

from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto
from common.lib.also import also


class FilteredResultMessageFormatter:
    _dict_id: int = None
    _config: dict = {}

    def __init__(
            self,
            clean_data_params_dictionary: ClearingDictionary,
            config
    ):
        self._clean_data_params_dictionary = clean_data_params_dictionary
        self._dict_id = self._clean_data_params_dictionary.select_by_id('b_url')
        self._config = config

    def format(self, filtered_data: list[FilteredResultDto]):
        result_list = reduce(self._format_url, filtered_data, [])
        return '\n ===== \n'.join(str(x) for x in result_list)

    def _format_url(self, acc: list, item):
        next_val = self._find_url(item.clean_data.param_set)
        return also(acc, lambda x: acc.append(self._config['baseUrl'] + next_val))

    def _find_url(self, param_set: list[CleanDataParamDto]) -> str:
        result = next(x for x in param_set if x.type == self._dict_id)
        return result.value if result is not None else ''
