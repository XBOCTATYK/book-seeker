from apps.analyser.models.db.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class ClearingDictionary(DbDictionary):
    def __init__(self, data_source: DbLikeDataSource):
        super(ClearingDictionary, self).__init__(data_source, CleanDataParamsDictionaryDto)
