from sqlalchemy import Connection
from sqlalchemy.orm import Session

from datasource.providers.DataProvider import DataProvider


class DbLikeDataSource:
    name: str = None
    _session: Session = None
    _data_provider: DataProvider = None

    def __init__(self, data_provider: DataProvider, name: str = 'db_like_data_source'):
        self._data_provider = data_provider
        self._session = data_provider.connect()
        self.name = name

    def open_session(self) -> Session:
        return self._data_provider.create_session()

    def get_connection(self) -> Connection:
        return self._data_provider.get_connection()


