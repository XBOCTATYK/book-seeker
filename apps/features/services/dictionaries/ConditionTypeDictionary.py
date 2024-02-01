from apps.features.model.db.ConditionTypeDto import ConditionTypeDto
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class ConditionTypeDictionary(DbDictionary):
    def __init__(self, data_source: DbLikeDataSource):
        super(ConditionTypeDictionary, self).__init__(data_source, ConditionTypeDto)