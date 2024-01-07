from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary
from common.services.AbstractRepository import AbstractRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class FetchOptionsRepository(AbstractRepository):
    _filter_type_dictionary: FilterTypeDictionary = None

    def __init__(self, data_source: DbLikeDataSource, filter_type_dictionary: FilterTypeDictionary):
        super().__init__(data_source)
        self._filter_type_dictionary = filter_type_dictionary

    def insert_values(self, values: List[dict]):
        result_set = []

        for item in values:
            result_set.append(
                self.call_in_transaction(
                    lambda sess: self._insert_values(sess, item)
                )
            )

        return result_set

    def _insert_values(self, sess: Session, item: dict):
        filter_values_to_insert = []

        value_to_insert = {
            'checkin': item['checkin'],
            'checkout': item['checkout'],
            'currency': item['currency'],
            'map_box': item['map_box'],
            'is_active': True
        }
        options_insert_statement = (insert(FetchOptionsTable).values(value_to_insert)
                                    .returning(FetchOptionsTable.id))
        inserted_id = sess.execute(options_insert_statement).scalar_one_or_none()

        filter_insert = []

        if item['filters'] is not None:
            for (key, value) in item['filters'].items():
                filter_values_to_insert.append({
                    'value': value if value is not None else '1',
                    'type': self._filter_type_dictionary.select_by_id(key),
                    'fetch_options': inserted_id
                })

            filter_insert_statement = (insert(FilterOptionsTable).values(filter_values_to_insert)
                                       .returning(FilterOptionsTable.id))

            filter_insert = sess.execute(filter_insert_statement).scalars().all()

        return {'id': inserted_id, 'filters': filter_insert}
