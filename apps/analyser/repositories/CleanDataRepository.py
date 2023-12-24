from DateTime import DateTime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from apps.analyser.models.ECleanDataStatus import ECleanDataStatus
from apps.analyser.models.db.CleanDataDto import CleanDataDto
from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from apps.analyser.models.types.ClearDataInsertItem import ClearDataInsertItem
from common.services.AbstractRepository import AbstractRepository


class CleanDataRepository(AbstractRepository):
    def insert_clear_data(self, values: list[ClearDataInsertItem]) -> CleanDataDto:
        return self.call_in_transaction(lambda sess: self._insert_clear_data(sess, values))

    def _insert_clear_data(self, sess: Session, values: list[ClearDataInsertItem]) -> CleanDataDto:
        insert_clear_data_statements = insert(CleanDataDto)\
            .values({'status': ECleanDataStatus.NEW.value, 'created_at': DateTime().ISO(), 'updated_at': DateTime().ISO()})\
            .returning(CleanDataDto.id)
        param_set = sess.execute(insert_clear_data_statements).scalar_one_or_none()

        result_values_set = list(map(lambda x: {'param_set': param_set, 'type': x['type'], 'value': x['value']}, values))
        insert_values_statements = insert(CleanDataParamDto).values(result_values_set)
        sess.execute(insert_values_statements)

        req = select(CleanDataDto).where(CleanDataDto.id == param_set)
        rest: CleanDataDto = sess.execute(req).unique().scalar_one_or_none()

        return rest

    def get_all(self) -> list[CleanDataDto]:
        session = self.get_current_session()
        statement = select(CleanDataDto)
        return list(session.execute(statement).unique().scalars().all())

