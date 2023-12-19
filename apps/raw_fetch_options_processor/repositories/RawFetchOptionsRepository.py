from typing import List, Callable, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.raw_fetch_options_processor.model.db.RawFetchOptionsDto import RawFetchOptionsDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class RawFetchOptionsRepository(AbstractRepository):
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._offset_pointer_repository = offset_pointer_repository

    def process_next_n_records(self, count: int, fn: Callable[[List[RawFetchOptionsDto]], T]) -> T:
        return self.call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_in_window(
                count,
                lambda low, top: self._process_next_n_records(sess, low, top, fn)
            )
        )

    def _process_next_n_records(self, sess: Session, low: int, top: int, fn: Callable[[List[RawFetchOptionsDto]], T]) -> T:
        record_list = self._find_next_n_records(sess, low, top)
        print(f'Found {len(record_list)} raw fetch options!')
        return fn(record_list)

    def _find_next_n_records(self, sess: Session, low: int, top: int) -> List[RawFetchOptionsDto]:
        search_statement = select(RawFetchOptionsDto).where(RawFetchOptionsDto.id >= low) \
            .where(RawFetchOptionsDto.id < top).with_for_update(skip_locked=True)
        raw_fetch_options_db_result = sess.execute(search_statement)

        return list(raw_fetch_options_db_result.scalars().all())

    def save(self, raw_fetch_options_dto: RawFetchOptionsDto) -> int:
        return self.call_in_transaction(lambda sess: self._save(sess, raw_fetch_options_dto))

    def _save(self, sess: Session, raw_fetch_options_dto: RawFetchOptionsDto) -> int:
        sess.add(raw_fetch_options_dto)
        sess.flush([raw_fetch_options_dto])
        print(f'Saved {len(raw_fetch_options_dto.url)}!')

        return raw_fetch_options_dto.id
