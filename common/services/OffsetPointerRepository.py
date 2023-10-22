from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from common.model.db.OffsetPointerDto import OffsetPointerDto
from common.services.AbstractRepository import AbstractRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class OffsetPointerRepository(AbstractRepository):
    _data_source = None
    _session: Session = None
    _repository_name = None

    def __init__(self, data_source: DbLikeDataSource, repo_name: str):
        super().__init__(data_source)
        self._data_source = data_source
        self._repository_name = repo_name

    def get_offset(self):
        return self._eval(self._get_by_key)

    def update_value(self, value: str):
        return self._eval_in_transaction(lambda sess: self._save(sess, value))

    def _get_by_key(self, sess: Session):
        offset_search_statement = select(OffsetPointerDto).where(OffsetPointerDto.key == self._repository_name)
        offset_db_result = sess.execute(offset_search_statement)
        offset = offset_db_result.one_or_none()

        if offset is None:
            self._insert_new_record(sess)
            offset = 0

        return offset

    def _insert_new_record(self, sess: Session):
        insert_statement = insert(OffsetPointerDto).values({'key': self._repository_name, 'value': 0, 'is_active': True})
        return sess.execute(insert_statement)

    def _save(self, sess: Session, value: str):
        offset_statement = update(OffsetPointerDto) \
            .where(OffsetPointerDto.key == self._repository_name)

        sess.execute(offset_statement, {'value': value})
