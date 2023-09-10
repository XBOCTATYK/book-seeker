from sqlalchemy.orm import Session

from common.model.db.RawOptionsDataDto import RawOptionsDataDto
from datasource.DbDataSource import DbDataSource


class RawDataRepository:
    data_source: DbDataSource = None

    def __init__(self, data_source: DbDataSource):
        self.data_source = data_source

    def save(self, raw_options_data_dto: RawOptionsDataDto):
        session: Session = self.data_source.get_session()

        session.begin()
        session.add(raw_options_data_dto)
        session.commit()
