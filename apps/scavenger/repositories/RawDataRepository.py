from typing import Optional, List, TypeVar, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.scavenger.models.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class RawDataRepository(AbstractRepository):
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._offset_pointer_repository = offset_pointer_repository

    def save(self, raw_options_data_dto: RawOptionsDataDto) -> int:
        return self._call_in_transaction(lambda sess: sess.add(raw_options_data_dto))

    def save_all(self, list_dto: List[RawOptionsDataDto]):
        return self._call_in_transaction(lambda sess: self._save_all(sess, list_dto))

    def find_next(self) -> Optional[RawOptionsDataDto]:
        return self._call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_at_offset(
                lambda offset: self._find_next(sess, offset)
            )
        )

    def find_next_n(self, count: int) -> List[RawOptionsDataDto]:
        return self._call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_in_window(
                count,
                lambda low, top: self._find_next_n(sess, low, top)
            )
        )

    def process_next(self, fn: Callable[[RawOptionsDataDto], T]) -> T:
        return self._call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_at_offset(
                lambda offset: self._process_next(sess, offset, fn)
            )
        )

    def process_next_n(self, count: int, fn: Callable[[List[RawOptionsDataDto]], T]) -> T:
        return self._call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_in_window(
                count,
                lambda low, top: self._process_next_n(sess, low, top, fn)
            )
        )

    def _save_all(self, sess: Session, list_dto: List[RawOptionsDataDto]):
        sess.add_all(list_dto)
        sess.flush(list_dto)

    def _find_next(self, sess: Session, offset: int) -> Optional[RawOptionsDataDto]:
        search_statement = select(RawOptionsDataDto)\
            .where(RawOptionsDataDto.id == offset)\
            .with_for_update(skip_locked=True)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_dto_set = raw_data_db_result.one_or_none()

        raw_data_dto = raw_data_dto_set[0]

        return raw_data_dto

    def _find_next_n(self, sess: Session, low: int, top: int) -> List[RawOptionsDataDto]:
        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id >= low) \
            .where(RawOptionsDataDto.id < top).with_for_update(skip_locked=True)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_column_set = raw_data_db_result.all()

        raw_data_dto_list = list(map(lambda x: x[0], raw_data_column_set))

        return raw_data_dto_list

    def _process_next(self, sess: Session, offset: int, fn: Callable[[RawOptionsDataDto], T]) -> T:
        raw_data_dto = self._find_next(sess, offset)
        result = fn(raw_data_dto)

        return result

    def _process_next_n(self, sess: Session, low: int, top: int, fn: Callable[[List[RawOptionsDataDto]], T]) -> T:
        raw_data_dto_list = self._find_next_n(sess, low, top)
        result = fn(raw_data_dto_list)

        return result
