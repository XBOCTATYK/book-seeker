from typing import Optional

from sqlalchemy import Connection
from sqlalchemy.orm import Session

from datasource.providers.DataProvider import DataProvider


class DbLikeDataSource:
    name: str = None
    _session: Optional[Session] = None
    _data_provider: DataProvider = None

    def __init__(self, data_provider: DataProvider, name: str = 'db_like_data_source'):
        self._data_provider = data_provider
        self.name = name

    def open_session(self) -> Session:
        if self._session is None or not self._session.in_transaction():
            self._session = self._data_provider.create_session()

        return self._session

    def close_session(self):
        if self._session is not None and not self._session.in_transaction():
            self._session.close()
            self._session = None

    def get_connection(self) -> Connection:
        return self._data_provider.get_connection()

    def get_provider(self) -> DataProvider:
        return self._data_provider


