from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource


class FilterTypeDictionary(DbDictionary):
    def __init__(self, data_source: DbLikeDataSource):
        super(FilterTypeDictionary, self).__init__(data_source, FilterTypesTable)
