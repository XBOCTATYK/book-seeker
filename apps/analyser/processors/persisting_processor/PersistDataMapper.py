from common.services.DbDictionary import DbDictionary
from pydash import get, split


class PersistDataMapper:
    _dictionary: DbDictionary

    def __init__(self, dictionary: DbDictionary):
        self._dictionary = dictionary

    def to_insert_list(self, data: dict) -> list:
        selectors = self._dictionary.values()
        values = []

        for selector in selectors:
            selector_parts = split(selector, '.')
            values.append({'type': self._dictionary.select_by_id(selector), 'value': get(data, selector_parts)})

        filtered_values = list(filter(lambda x: x['value'] is not None, values))

        return filtered_values
