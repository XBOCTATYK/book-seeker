from functools import reduce

from apps.scavenger.models.logic import FilterOptions


class FilterOptionsSerializer:
    mappers = [
        lambda x: f"review_score={x['review_score']*10};" if 'review_score' in x else '',
        lambda x: f"oos={x['oos']};" if 'oos' in x and x['oos'] != '-1' else '',
        lambda x: f"rooms={x['rooms']};" if 'rooms' in x and x['rooms'] != '-1' else '',
        lambda x: f"price={x['currency']}-{x['min_price']}-{x['max_price']}-1" if 'currency' in x else '',
    ]

    def serialize(self, filter_options: FilterOptions) -> str:
        return self._apply_str_mappers(filter_options)

    def _apply_str_mappers(self, filter_options: FilterOptions) -> str:
        return reduce(lambda acc, item: acc + item(filter_options), self.mappers, '')
