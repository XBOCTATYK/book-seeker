from functools import reduce

from apps.scavenger.models.logic import FilterOptions


def create_default_numeric_mapper(name: str, modifier=lambda x: x):
    return lambda x: f"{name}={modifier(x[name])};" if name in x else ''


def create_bool_mapper(name: str, modifier=lambda x: x):
    return lambda x: f"{modifier(name)};" if name in x else ''


class FilterOptionsSerializer:
    mappers = [
        create_default_numeric_mapper('review_score', lambda x: x * 10),
        create_default_numeric_mapper('oos'),
        create_default_numeric_mapper('rooms'),
        create_bool_mapper('fc=2'),  # free cancellation
        create_bool_mapper('fc=4'),  # without card
        create_bool_mapper('fc=5'),  # no prepayment
        create_bool_mapper('roomfacility=11'),  # 11 - air cond
        create_bool_mapper('roomfacility=38'),  # 38 - bathroom
        create_bool_mapper('hotelfacility=107'),  # wifi
        create_default_numeric_mapper('distance'),
        create_default_numeric_mapper('entire_place_bedroom_count'),
        lambda x: f"price={x['currency']}-{x['min_price']}-{x['max_price']}-1" if 'currency' in x else '',
    ]

    def serialize(self, filter_options: FilterOptions) -> str:
        return self._apply_str_mappers(filter_options)

    def _apply_str_mappers(self, filter_options: FilterOptions) -> str:
        return reduce(lambda acc, item: acc + item(filter_options), self.mappers, '')
