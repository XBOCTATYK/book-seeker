from apps.analyser.models.db.ParamWeightDto import ParamWeightDto
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class WeightDictionary(DbDictionary):
    def __init__(self, data_source: DbLikeDataSource):
        super(WeightDictionary, self).__init__(data_source, ParamWeightDto)
