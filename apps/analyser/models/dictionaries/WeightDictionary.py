from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.analyser.models.db.ParamWeightDto import ParamWeightDto
from common.services.AbstractRepository import AbstractRepository
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class WeightDictionary(AbstractRepository):
    _weights = []

    def __init__(self, data_source: DbLikeDataSource):
        super().__init__(data_source)
        self._fill_dictionary()

    def _fill_dictionary(self):
        items = self._eval(self._fill_dictionary_db)

        for item in items:
            self._weights.append(item)

    def _fill_dictionary_db(self, sess: Session):
        statement = select(ParamWeightDto).where(ParamWeightDto.id > 0)
        return sess.execute(statement).scalars().all()

    def values(self) -> List[ParamWeightDto]:
        return self._weights
