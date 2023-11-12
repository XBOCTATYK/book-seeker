from sqlalchemy import select
from typing import List, Callable, TypeVar

from sqlalchemy.orm import Session

from apps.raw_fetch_options_processor.model.db.RawFetchOptions import RawFetchOptions
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class RawFetchOptionsRepository(AbstractRepository):
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._offset_pointer_repository = offset_pointer_repository

    def process_next_n_records(self, count: int, fn: Callable[[List[RawFetchOptions]], T]) -> T:
        return self._offset_pointer_repository.call_in_window(
            count,
            lambda low, top: self._call_in_transaction(
                lambda sess: self._process_next_n_records(sess, low, top, fn)
            )
        )

    def _process_next_n_records(self, sess: Session, low: int, top: int, fn: Callable[[List[RawFetchOptions]], T]) -> T:
        record_list = self._find_next_n_records(sess, low, top)
        return fn(record_list)

    def _find_next_n_records(self, sess: Session, low: int, top: int) -> List[RawFetchOptions]:
        search_statement = select(RawFetchOptions).where(RawFetchOptions.id >= low) \
            .where(RawFetchOptions.id < top).with_for_update(skip_locked=True)
        raw_fetch_options_db_result = sess.execute(search_statement)

        return list(raw_fetch_options_db_result.scalars().all())
