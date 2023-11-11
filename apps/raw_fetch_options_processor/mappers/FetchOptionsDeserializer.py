from apps.scavenger.models.constants.filter_types_enum import EFilterType


def map_field(name: str, modifier=lambda x: x):
    return lambda x: modifier(name) if name in x else ''


class FetchOptionsDeserializer:
    filter_mappers = dict(map(lambda val: (val, map_field(val)), EFilterType.values()))
    mappers = {
        'checkin': map_field('checkin'),
        'checkout': map_field('checkout'),
        'currency': map_field('currency'),
        'map_box': map_field('ltfd_excl', lambda val: val.replace(';BBOX=', '')),
    }

    def deserialize(self, values: dict) -> dict:
        self.mappers.setdefault('filters', map_field('nflt', self._set_filters))

        self.filter_mappers.setdefault(('min_price', map_field('price', lambda x: x.split('-')[1])))
        self.filter_mappers.setdefault(('max_price', map_field('price', lambda x: x.split('-')[2])))
        self.filter_mappers.setdefault(('review_score', map_field('review_score', lambda x: x/10)))

        result = {}
        for (name, mapper) in self.mappers:
            result.setdefault(name, mapper(values[name]))

        return result

    def _set_filters(self, filter_values_str: str) -> dict[any]:
        filters = filter_values_str.split(';')
        filters_dict = dict(map(self._split_filter, filters))

        result = {}
        for (key, filter_maper) in self.filter_mappers.items():
            result.setdefault(key, filter_maper(filters_dict[key] if key in filters_dict else None))

        return result

    def _split_filter(self, filter_str: str) -> tuple[str, str]:
        filter_item = filter_str.split('=')
        return filter_item[0], filter_item[1]

