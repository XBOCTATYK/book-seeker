from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.lib.db.offset_functions import find_element_with_minimal_id_more_than_current
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource



class RawDataRepository(AbstractRepository):
    data_source: DbLikeDataSource = None
    _session: Session = None
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self.data_source = data_source
        self._offset_pointer_repository = offset_pointer_repository

    def save(self, raw_options_data_dto: RawOptionsDataDto) -> int:
        return self._eval_in_transaction(lambda sess: sess.add(raw_options_data_dto))

    def save_all(self, list_dto: List[RawOptionsDataDto]):
        return self._eval_in_transaction(lambda sess: self._save_all(sess, list_dto))

    def find_next(self) -> Optional[RawOptionsDataDto]:
        return self._eval_in_transaction(self._find_next)

    def find_next_n(self, count: int) -> List[RawOptionsDataDto]:
        return self._eval_in_transaction(lambda sess: self._find_next_n(sess, count))

    def _save_all(self, sess: Session, list_dto: List[RawOptionsDataDto]):
        sess.add_all(list_dto)
        sess.flush(list_dto)

    def _find_next(self, sess: Session) -> Optional[RawOptionsDataDto]:
        offset = self._offset_pointer_repository.get_offset()

        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id == offset)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_dto_set = raw_data_db_result.one_or_none()

        # sets minimal found id if element wasn't found
        if raw_data_dto_set is None:
            raw_data_dto_set = find_element_with_minimal_id_more_than_current(sess, RawOptionsDataDto, offset)

        if raw_data_dto_set is None:
            return None

        raw_data_dto = raw_data_dto_set[0]
        self._offset_pointer_repository.update_value(raw_data_dto.id + 1)

        return raw_data_dto

    def _find_next_n(self, sess: Session, count: int) -> List[RawOptionsDataDto]:
        offset = self._offset_pointer_repository.get_offset()
        next_offset = offset + count

        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id >= offset)\
            .where(RawOptionsDataDto.id < next_offset)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_column_set = raw_data_db_result.all()

        self._offset_pointer_repository.update_value(next_offset)
        raw_data_dto_list = list(map(lambda x: x[0], raw_data_column_set))

        return raw_data_dto_list
