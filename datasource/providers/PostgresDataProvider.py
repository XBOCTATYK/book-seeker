from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

from datasource.configs.DbConfig import DbConfig
from datasource.providers.DataProvider import DataProvider


def create_db_connect_url(db_config: DbConfig):
    return URL.create(
        "postgresql+" + db_config['engine'],
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database'],
        username=db_config['user'],
        password=db_config['password']
    )


class PostgresDataProvider(DataProvider):
    config: DbConfig = None
    engine = None
    connection = None

    def __init__(self, config: DbConfig):
        super().__init__()
        if config is None:
            raise AssertionError("Config cannot be None")

        self.config = config
        self.engine = create_engine(create_db_connect_url(config))

    def connect(self):
        connection = self._create_or_get_connection()
        return Session(connection)

    def get_connection(self):
        return self._create_or_get_connection()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

        return self

    def create_session(self) -> Session:
        return Session(self.engine)

    def _create_or_get_connection(self):
        if self.connection is None:
            self.connection = self.engine.connect()\
                .execution_options(schema_translate_map={None: self.config['scheme']})

        return self.connection
