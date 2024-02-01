from sqlalchemy.orm import Session

from apps.features.model.EConditionTypes import EConditionTypes
from apps.features.model.db.ConditionDto import ConditionDto
from common.model.db.DictionaryDto import DictionaryDto
from common.services.AbstractRepository import AbstractRepository
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class ConditionRepository(AbstractRepository):
    _condition_type_dictionary: DbDictionary = None
    _condition_operator_dictionary: DbDictionary = None

    def __init__(
            self,
            data_source: DbLikeDataSource,
            condition_type_dictionary: DbDictionary,
            condition_operator_dictionary: DbDictionary
    ):
        super().__init__(data_source)
        self._condition_type_dictionary = condition_type_dictionary
        self._condition_operator_dictionary = condition_operator_dictionary

    def get_by_type(self, condition_type: EConditionTypes) -> list[ConditionDto]:
        return self.eval(
            lambda session: self._get_by_type(session, condition_type.value)
        )

    def _get_by_type(self, session: Session, condition_type: str) -> list[ConditionDto]:
        condition_type: int = self._condition_type_dictionary.select_by_id(condition_type)
        return session.query(ConditionDto).filter(ConditionDto.condition_type_id == condition_type).all()
