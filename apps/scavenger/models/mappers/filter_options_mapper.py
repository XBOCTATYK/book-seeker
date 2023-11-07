from functools import reduce

from apps.scavenger.models.constants.filter_types_enum import EFilterType


def create_default_numeric_mapper(name: str, modifier=lambda x: x):
    return lambda x: f"{name}={modifier(x[name])};" if name in x else ''


def create_bool_mapper(name: str, modifier=lambda x: x):
    return lambda x: f"{modifier(name)};" if name in x else ''


class FilterOptionsSerializer:
    mappers = [
        create_default_numeric_mapper(EFilterType.REVIEW_SCORE.value[0], lambda x: x * 10),
        create_default_numeric_mapper(EFilterType.ONLY_AVAILABLE.value[0]),
        create_default_numeric_mapper(EFilterType.ROOMS.value[0]),
        create_bool_mapper(EFilterType.FREE_CANCELLATION.value[0]),
        create_bool_mapper(EFilterType.WITHOUT_CARD.value[0]),
        create_bool_mapper(EFilterType.NO_PREPAYMENT.value[0]),
        create_bool_mapper(EFilterType.AIR_COND.value[0]),
        create_bool_mapper(EFilterType.PRIVATE_BATHROOM.value[0]),
        create_bool_mapper(EFilterType.FREE_WIFI.value[0]),
        create_default_numeric_mapper(EFilterType.DISTANCE.value[0]),
        create_default_numeric_mapper(EFilterType.ROOMS_COUNT.value[0]),
        lambda x: f"price={x[EFilterType.CURRENCY.value[0]]}-{x[EFilterType.MIN_PRICE.value[0]]}-{x[EFilterType.MAX_PRICE.value[0]]}-1" if EFilterType.CURRENCY.value[0] in x else '',
    ]

    def serialize(self, filter_options: dict) -> str:
        return self._apply_str_mappers(filter_options)

    def _apply_str_mappers(self, filter_options: dict) -> str:
        return reduce(lambda acc, item: acc + item(filter_options), self.mappers, '')
