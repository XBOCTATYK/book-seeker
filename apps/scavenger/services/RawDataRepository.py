from sqlalchemy import select, update
from sqlalchemy.orm import Session

from common.model.db.OffsetPointerDto import OffsetPointerDto
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

    def save(self, raw_options_data_dto: RawOptionsDataDto):
        return self._eval_in_transaction(lambda sess: sess.add(raw_options_data_dto))

    def get_next(self):
        return self._eval_in_transaction(self._get_next)

    def _get_next(self, sess: Session) -> RawOptionsDataDto:
        offset = self._offset_pointer_repository.get_offset()

        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id == offset)
        raw_data_db_result = sess.execute(search_statement)
        raw_data_dto, *rest = raw_data_db_result.first()

        self._offset_pointer_repository.update_value(offset + 1)

        return raw_data_dto
