from common.services.DbDictionary import DbDictionary
from pydash import get, split


class ClearDataSelectorService:
    _dictionary: DbDictionary

    def __init__(self, dictionary: DbDictionary):
        self._dictionary = dictionary

    def select_to_dict(self, data: dict) -> dict[str, str]:
        selectors = self._dictionary.values()
        output_dict = {}

        for selector in selectors:
            selector_parts = split(selector, '.')
            output_dict.setdefault(selector, get(data, selector_parts))

        return output_dict
