from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource


# TODO: extract it to a separate file
def find_element_with_minimal_id(sess: Session):
    additional_search_statement = select(RawOptionsDataDto).order_by(RawOptionsDataDto.id).limit(1)
    raw_data_db_result = sess.execute(additional_search_statement)
    return raw_data_db_result.one_or_none()


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

    def find_next(self) -> Optional[RawOptionsDataDto]:
        return self._eval_in_transaction(self._find_next)

    def _find_next(self, sess: Session) -> Optional[RawOptionsDataDto]:
        offset = self._offset_pointer_repository.get_offset()

        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id == offset)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_dto_set = raw_data_db_result.one_or_none()

        # sets minimal found id if element wasn't found
        if raw_data_dto_set is None:
            raw_data_dto_set = find_element_with_minimal_id(sess)

        if raw_data_dto_set is None:
            return None

        raw_data_dto = raw_data_dto_set[0]
        self._offset_pointer_repository.update_value(raw_data_dto.id + 1)

        return raw_data_dto
