from sqlalchemy import select
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
        session: Session = self._data_source.open_session()
        statement = select(AppConfigDto).where(AppConfigDto.is_active == True)
        params_collection = session.execute(statement).all()

        for param in params_collection:
            dto = param[0]
            print(dto)
            raw_config.append([dto.key, dto.value])

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

        session.close()

        return config
