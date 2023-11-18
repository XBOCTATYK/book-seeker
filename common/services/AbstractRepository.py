from abc import ABC

from sqlalchemy.orm import Session

from datasource.DbLikeDataSource import DbLikeDataSource


class AbstractRepository(ABC):
    _data_source = None
    _session: Session = None

    def __init__(self, data_source: DbLikeDataSource):
        self._data_source = data_source

    def _get_current_session(self):
        return self._data_source.open_session()

    def _eval(self, fn):
        session: Session = self._data_source.open_session()
        result = fn(session)

        session.expunge_all()
        session.commit()
        self._data_source.close_session()
        return result

    def _call_in_transaction(self, fn):
        session: Session = self._data_source.open_session()
        is_transaction_started_earlier = session.in_transaction()

        try:
            if not is_transaction_started_earlier:
                session.begin()

            result = fn(session)
            session.expunge_all()

            if not is_transaction_started_earlier:
                session.commit()

            return result

        except Exception as error:
            session.rollback()
            raise error
        finally:
            self._data_source.close_session()



