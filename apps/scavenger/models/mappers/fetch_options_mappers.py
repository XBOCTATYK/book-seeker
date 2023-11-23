from dataclasses import dataclass
from functools import reduce
from re import split
from typing import Callable, TypeVar, List

from DateTime import DateTime

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.models.logic.Coordinate import Coordinate
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary
from common.lib.also import also

T = TypeVar('T')


@dataclass
class EmptyValue:
    value: any


def find_element(func: Callable[[T], bool], collection: List[T]) -> T:
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

    def from_entity(self, fetch_options_table: FetchOptionsTable) -> FetchOptions:
        filters = self._filters_mapper.from_entity(fetch_options_table)

        return FetchOptions(
            map_box=self._parse_map_box(fetch_options_table.map_box),
            checkin=DateTime(fetch_options_table.checkin),
            checkout=DateTime(fetch_options_table.checkout),
            currency=fetch_options_table.currency,
            filter=filters,
            persons=3
        )

    def _parse_map_box(self, map_box: str) -> MapViewBox:
        map_box_arr = split(',', map_box)
        return MapViewBox(
            Coordinate(map_box_arr[0], map_box_arr[1]),
            Coordinate(map_box_arr[2], map_box_arr[3]),
        )

    class FiltersMapper:
        _filter_type_dictionary: FilterTypeDictionary

        def __init__(self, filter_type_dictionary: FilterTypeDictionary):
            self._iterating_filters = None
            self._filter_type_dictionary = filter_type_dictionary

        def search_by_name(self, name: str, collection: list[FilterOptionsTable]) -> FilterOptionsTable:
            return find_element(lambda item: item.type == self._filter_type_dictionary.select_by_id(name), collection)

        def from_entity(self, fetch_options_table: FetchOptionsTable) -> dict[str]:
            filters = fetch_options_table.filters

            filter_options = reduce(
                lambda acc, item: also(
                    acc,
                    lambda _: acc.setdefault(item, str(self.search_by_name(item, filters).value))
                ),
                self._filter_type_dictionary.values(),
                {}
            )

            return filter_options
