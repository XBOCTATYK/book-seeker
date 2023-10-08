from sqlalchemy import select, update
from sqlalchemy.orm import Session

from common.model.db.OffsetPointerDto import OffsetPointerDto
from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.DbLikeDataSource import DbLikeDataSource


class RawDataRepository:
    data_source: DbLikeDataSource = None
    _session: Session = None
    _repository_name = 'scavenge_app'

    def __init__(self, data_source: DbLikeDataSource):
        self.data_source = data_source

    def save(self, raw_options_data_dto: RawOptionsDataDto):
        self._eval_in_transaction(lambda sess: sess.add(raw_options_data_dto))

    def get_first(self):
        self._eval_in_transaction(self._get_first)

    def _get_current_session(self) -> Session:
        return self.data_source.open_session() if self._session is None else self._session

    def _eval_in_transaction(self, fn):
        session: Session = self._get_current_session()

        session.begin()
        result = fn(session)

        session.commit()

        self._session = session

        return result

    def _get_first(self, sess: Session) -> RawOptionsDataDto:
        offset_search_statement = select(OffsetPointerDto).where(OffsetPointerDto.key == self._repository_name)
        offset_db_result = sess.execute(offset_search_statement)
        offset = offset_db_result.first()[0].value

        search_statement = select(RawOptionsDataDto).where(RawOptionsDataDto.id == offset)
        result = sess.execute(search_statement)
        eventual, *rest = result.first()

        offset_statement = update(OffsetPointerDto)\
            .where(OffsetPointerDto.key == self._repository_name)
        sess.execute(offset_statement, {'value': offset + 1})

        return eventual
