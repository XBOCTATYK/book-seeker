from sqlalchemy.orm import Session

from datasource.DbLikeDataSource import DbLikeDataSource


class AbstractRepository:
    _data_source = None
    _session: Session = None

    def __init__(self, data_source: DbLikeDataSource):
        self._data_source = data_source

    def _get_current_session(self) -> Session:
        if self._session is None:
            session = self._data_source.open_session()
        else:
            session = self._session

        self._session = session
        return session

    def _eval_in_transaction(self, fn):
        session: Session = self._get_current_session()
        is_transaction_started_earlier = session.get_transaction().is_active if session.get_transaction() else False

        try:
            if not is_transaction_started_earlier:
                session.begin()

            result = fn(session)

            if not is_transaction_started_earlier:
                session.commit()

            return result

        except:
            session.rollback()


