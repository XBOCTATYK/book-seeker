from sqlalchemy.orm import Session

from common.model.db.AppConfigDto import AppConfigDto
from configlib.formatters.ConfigFormatter import ConfigFormatter
from datasource.DbDataSource import DbDataSource


class DbConfigFormatter(ConfigFormatter):
    _data_source: DbDataSource = None

    def __init__(self, data_source: DbDataSource):
        self._data_source = data_source

    def get_config(self) -> dict:
        raw_config = []
        session: Session = self._data_source.get_session()
        params_collection = session.execute(AppConfigDto.__table__.select()).all()

        for param in params_collection:
            param_id, key, value, is_active, dt, ut = param
            raw_config.append([key, value])

        config = {}
        for config_part in raw_config:
            key, value = config_part
            key_array = key.split('.')

            current = config
            for index, part in enumerate(key_array):
                if index == len(key_array) - 1:
                    current.setdefault(part, value)
                else:
                    current.setdefault(part, {})
                    current = current[part]

        return config
