from dataclasses import dataclass
from typing import Optional

from DateTime import DateTime

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary


@dataclass
class EmptyValue:
    value: any


def find_element(func, collection):
    found_item = EmptyValue(-1)

    for item in collection:
        if func(item):
            found_item = item
            break

    return found_item


class FetchOptionsMapper:
    _filters_mapper = None

    def __init__(self, filter_type_dictionary: FilterTypeDictionary):
        self._filters_mapper = self.FiltersMapper(filter_type_dictionary)

    def from_entity(self, fetch_options_table: FetchOptionsTable):
        filters = self._filters_mapper.from_entity(fetch_options_table)

        return FetchOptions(
            map_box=fetch_options_table.map_box,
            checkin=DateTime(fetch_options_table.checkin),
            checkout=DateTime(fetch_options_table.checkout),
            currency=fetch_options_table.currency,
            filter=filters
        )

    class FiltersMapper:
        _filter_type_dictionary: FilterTypeDictionary

        def __init__(self, filter_type_dictionary: FilterTypeDictionary):
            self._filter_type_dictionary = filter_type_dictionary

        def search_by_name(self, name, collection):
            return find_element(lambda item: item.type == self._filter_type_dictionary.select_by_id(name), collection)

        def from_entity(self, fetch_options_table: FetchOptionsTable):
            filters = fetch_options_table.filters

            return FilterOptions(
                oos=str(self.search_by_name('oos', filters).value),
                rooms=self.search_by_name('rooms', filters).value,
                min_price=self.search_by_name('min_price', filters).value,
                max_price=self.search_by_name('max_price', filters).value,
                review_score=int(self.search_by_name('review_score', filters).value),
                currency=self.search_by_name('currency', filters).value,
            )
