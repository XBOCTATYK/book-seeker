from apps.features.model.db.ConditionOperatorsDto import ConditionOperatorsDto
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class ConditionOperatorDictionary(DbDictionary):
    def __init__(self, data_source: DbLikeDataSource):
        super(ConditionOperatorDictionary, self).__init__(data_source, ConditionOperatorsDto)