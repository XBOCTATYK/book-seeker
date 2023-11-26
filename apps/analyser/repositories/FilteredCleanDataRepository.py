from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.analyser.models.db.CleanDataDto import CleanDataDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class FilterCleanDataRepository(AbstractRepository):
    _offset_pointer_repository = None

    def __init__(self, data_source: DbLikeDataSource, offset_pointer_repository: OffsetPointerRepository):
        super().__init__(data_source)

        self._offset_pointer_repository = offset_pointer_repository

    def process_n_records(self, count: int, fn):
        return self.call_in_transaction(
            lambda sess: self._offset_pointer_repository.call_in_window(
                count,
                lambda bottom, top: self._process_n_records(sess, bottom, top, fn)
            )
        )

    def _process_n_records(self, sess: Session, bottom: int, top: int, fn):
        statement = (select(CleanDataDto).where(CleanDataDto.id >= bottom)
                     .where(CleanDataDto.id < top)
                     .with_for_update(skip_locked=True, key_share=True))

        clean_data_dtos = sess.execute(statement).scalars().all()

        print(f'Found {len(clean_data_dtos)} records to filter')
        return fn(clean_data_dtos)
