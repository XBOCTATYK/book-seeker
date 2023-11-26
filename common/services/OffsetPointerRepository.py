from typing import TypeVar, Callable, Type

from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import min

from common.model.db.BaseDto import BaseDto
from common.model.db.OffsetPointerDto import OffsetPointerDto
from common.services.AbstractRepository import AbstractRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class OffsetPointerRepository(AbstractRepository):
    _data_source = None
    _session: Session = None
    _repository_name = None

    def __init__(self, data_source: DbLikeDataSource, repo_name: str):
        super().__init__(data_source)
        self._data_source = data_source
        self._repository_name = repo_name

    def get_name(self) -> str:
        return self._repository_name

    def get_offset(self):
        return self.call_in_transaction(self._get_by_key)

    def update_value(self, value: int):
        self.call_in_transaction(lambda sess: self._save(sess, value))

    def call_at_offset(self, fn: Callable[[int], T]):
        offset = self.get_offset()

        result = fn(offset)

        self.update_value(offset + 1)

        return result

    def call_in_window(self, count: int, fn: Callable[[int, int], T]) -> T:
        low_border = self.get_offset()
        top_border = low_border + count
        print(f'{self._repository_name}: trying to process items {low_border}-{top_border}')

        result = fn(low_border, top_border)

        if isinstance(result, list):
            top_border = low_border + len(result)

        print(f'{self._repository_name}: offset will be advance till {top_border}')
        self.update_value(top_border)

        return result

    def setup_offset(self, dto: Type[BaseDto]):
        return self.call_in_transaction(
            lambda sess: self._setup_offset(sess, dto)
        )

    def _get_by_key(self, sess: Session) -> int:
        offset_search_statement = (select(OffsetPointerDto)
                                   .where(OffsetPointerDto.key == self._repository_name)
                                   .where(OffsetPointerDto.is_active == True)
                                   .with_for_update(key_share=True)
                                   )
        offset_db_result = sess.execute(offset_search_statement)
        offset = offset_db_result.scalar_one_or_none()

        if offset is None:
            self._insert_new_record(sess)
            sess.flush()
            offset = 0
        else:
            offset = offset.value

        return offset

    def _insert_new_record(self, sess: Session):
        insert_statement = insert(OffsetPointerDto) \
            .values({'key': self._repository_name, 'value': 0, 'is_active': True})

        sess.execute(insert_statement)

    def _save(self, sess: Session, value: int):
        offset_statement = update(OffsetPointerDto) \
            .where(OffsetPointerDto.key == self._repository_name)

        sess.execute(offset_statement, {'value': value})

    def _setup_offset(self, sess: Session, dto: Type[BaseDto]) -> int:
        offset = self.get_offset()

        if offset != 0:
            return offset

        first_id = sess.execute(min(dto.id)).scalar_one_or_none()

        if first_id is None:
            print(f'Not items to set the offset {self.get_name()}')
            return 0

        self.update_value(first_id)

        return first_id
