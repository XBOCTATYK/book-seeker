from apps.analyser.models.types.ClearDataInsertItem import ClearDataInsertItem
from common.services.DbDictionary import DbDictionary


class PersistDataMapper:
    _dictionary: DbDictionary

    def __init__(self, dictionary: DbDictionary):
        self._dictionary = dictionary

    def to_insert_list(self, data: dict) -> list[ClearDataInsertItem]:
        selectors = self._dictionary.values()
        values = []

        for selector in selectors:
            values.append({'type': self._dictionary.select_by_id(selector), 'value': data[selector]})

        filtered_values = list(filter(lambda x: x['value'] is not None, values))

        return filtered_values
