from typing import List

from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.mappers.fetch_options_mappers import FetchOptionsMapper
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource import DbLikeDataSource


class FilterFetcher(AbstractRepository):
    _data_source: DbLikeDataSource = None
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._data_source = data_source
        self._offset_pointer_repository = offset_pointer_repository

    def fetch(self):
        return self._call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_at_offset(
                lambda offset: self._fetch(sess, offset)
            )
        )

    def _fetch(self, sess: Session, offset: int):
        statement = (select(FetchOptionsTable)
                     .where(FetchOptionsTable.is_active)
                     .where(FetchOptionsTable.id == offset))
        res: FetchOptionsTable = sess.execute(statement).unique().scalar_one_or_none()

        if res is None:
            return None

        fetch_options = self._process(res)
        return fetch_options

    def _process(self, result: FetchOptionsTable) -> List[FetchOptions]:
        return FetchOptionsMapper(FilterTypeDictionary(self._data_source)).from_entity(result)
