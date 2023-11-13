from apps.scavenger.models.constants.filter_types_enum import EFilterType


def map_field(name: str, modifier=lambda x: x):
    return lambda x: modifier(x[name]) if name in x else None


class FetchOptionsDeserializer:
    _filter_mappers = dict(map(lambda val: (val, map_field(val)), EFilterType.values()))
    _mappers = {
        'checkin': map_field('checkin'),
        'checkout': map_field('checkout'),
        'currency': map_field('currency'),
        'map_box': map_field('ltfd_excl', lambda val: val.replace(';BBOX=', '')),
    }

    def deserialize(self, values: dict) -> dict:
        self._mappers.setdefault('filters', map_field('nflt', self._set_filters))
        self._mappers['rooms'] = map_field('room1')

        self._filter_mappers['min_price'] = map_field(
            'price',
            lambda x: x.split('-')[1] if x.split('-')[1] != 'min' else '0'
        )
        self._filter_mappers['max_price'] = map_field(
            'price',
            lambda x: x.split('-')[2] if x.split('-')[2] != 'max' else '99999'
        )
        self._filter_mappers['review_score'] = map_field('review_score', lambda x: str(int(x) / 10))

        result = {}
        for (name, mapper) in self._mappers.items():
            result.setdefault(name, mapper(values))

        return result

    def _set_filters(self, filter_values_str: str) -> dict[any]:
        filters = filter_values_str.split(';')
        filters_dict = dict(map(self._split_filter, filters))

        result = {}
        for (key, filter_maper) in self._filter_mappers.items():
            map_result = filter_maper(filters_dict)
            if map_result is not None:
                result.setdefault(key, map_result)

        return result

    def _split_filter(self, filter_str: str) -> tuple[str, str]:
        filter_item = filter_str.split('=')
        return filter_item[0], filter_item[1]
