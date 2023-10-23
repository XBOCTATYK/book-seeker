from typing import Callable, List, TypeVar

from sqlalchemy import select
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

    def process_next_n(self, count: int, fn: Callable[[List[FilteredResultDto]], T]) -> T:
        return self._call_in_transaction(lambda sess: self._process_next_n(sess, count, fn))

    def _process_next_n(self, sess: Session, count: int, fn: Callable[[List[FilteredResultDto]], T]) -> T:
        offset = self._offset_pointer_repository.get_offset()
        next_offset = offset + count

        search_statement = select(FilteredResultDto) \
            .where(FilteredResultDto.id >= offset) \
            .where(FilteredResultDto.id < next_offset)
        filtered_options_db_set = sess.execute(search_statement).all()

        filtered_options = list(map(lambda x: x[0], filtered_options_db_set))
        result = fn(filtered_options)

        self._offset_pointer_repository.update_value(next_offset)

        return result
