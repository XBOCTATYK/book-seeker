from sqlalchemy import select, String
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from datasource.DbDataSource import DbDataSource


class FilterTypeDictionary:
    _data_source: DbDataSource
    _filter_types: dict

    def __init__(self, data_source: DbDataSource):
        self._data_source = data_source
        session: Session = self._data_source.open_session()
        db_result = session.execute(select(FilterTypesTable)).all()

        self._filter_types = {}

        for filter_type in db_result:
            key: FilterTypesTable = filter_type[0]
            self._filter_types.setdefault(key.name, key.id)

    def select_by_id(self, type_name: str) -> int:
        return self._filter_types[type_name]

    def values(self):
        return list(map(lambda x: x, self._filter_types))
