from DateTime import DateTime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from apps.analyser.models.db.CleanDataDto import CleanDataDto
from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from common.services.AbstractRepository import AbstractRepository


class CleanDataRepository(AbstractRepository):
    def insert_clear_data(self, values: list):
        return self._call_in_transaction(lambda sess: self._insert_clear_data(sess, values))

    def _insert_clear_data(self, sess: Session, values: list):
        insert_clear_data_statements = insert(CleanDataDto)\
            .values({'status': 'NEW', 'created_at': DateTime().ISO(), 'updated_at': DateTime().ISO()})\
            .returning(CleanDataDto.id)
        param_set = sess.execute(insert_clear_data_statements).scalar_one_or_none()

        result_values_set = list(map(lambda x: {'param_set': param_set, 'type': x['type'], 'value': x['value']}, values))
        insert_values_statements = insert(CleanDataParamDto).values(result_values_set)
        sess.execute(insert_values_statements)

        req = select(CleanDataDto).where(CleanDataDto.id == param_set)
        rest = sess.execute(req).unique().scalar_one_or_none()

        return rest

    def get_all(self):
        session = self._get_current_session()
        statement = select(CleanDataDto)
        return session.execute(statement).unique().fetchall()

