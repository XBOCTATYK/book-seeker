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

    def __init__(self, filter_type_dictionary: FilterTypeDictionary, data_source: DbLikeDataSource):
        super().__init__(data_source)
        self._filter_type_dictionary = filter_type_dictionary

    def insert_values(self, values: List[dict]):
        result_set = []

        for item in values:
            result_set.append(
                self._call_in_transaction(
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
            'persons': item['persons']
        }
        options_insert_statement = insert(FetchOptionsTable).values(value_to_insert).returning(FetchOptionsTable.id)
        inserted_id = sess.execute(options_insert_statement)

        for (key, value) in item['filters']:
            filter_values_to_insert.append({
                'value': value,
                'type': self._filter_type_dictionary.select_by_id(key),
                'fetch_options': inserted_id
            })

        filter_insert_statement_ids = insert(FilterOptionsTable).returning(FilterOptionsTable.id)

        return {'id': inserted_id, 'filters': filter_insert_statement_ids}