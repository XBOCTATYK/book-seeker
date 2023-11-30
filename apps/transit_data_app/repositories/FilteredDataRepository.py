from typing import Callable, List, TypeVar

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class FilteredDataRepository(AbstractRepository):
    _offset_pointer_repository: OffsetPointerRepository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self.data_source = data_source
        self._offset_pointer_repository = offset_pointer_repository
        self._offset_pointer_repository.setup_offset(FilteredResultDto)

    def process_next_n(self, count: int, fn: Callable[[List[FilteredResultDto]], T]) -> T:
        return self.call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_in_window(
                10,
                lambda top, bottom: self._process_next_n(sess, top, bottom, fn)
            )

        )

    def _process_next_n(self, sess: Session, bottom: int, top: int, fn: Callable[[List[FilteredResultDto]], T]) -> T:
        search_statement = select(FilteredResultDto) \
            .where(FilteredResultDto.id >= bottom) \
            .where(FilteredResultDto.id < top)
        filtered_options = sess.execute(search_statement).unique().scalars().all()

        result = fn(list(filtered_options))

        return result

    def insert_filtered_data(self, filtered_data_ids: List[int]):
        return self.call_in_transaction(
            lambda sess: self._insert_filtered_data(sess, filtered_data_ids)
        )

    def _insert_filtered_data(self, sess: Session, filtered_data_ids: List[int]) -> List[int]:
        values_to_insert = list(map(lambda filtered_data_id: {'param_set': filtered_data_id}, filtered_data_ids))
        insert_statement = insert(FilteredResultDto).values(values_to_insert).returning(FilteredResultDto.id)

        return list(sess.execute(insert_statement).scalars().all())

