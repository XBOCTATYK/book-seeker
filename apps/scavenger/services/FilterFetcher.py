from typing import Sequence, List

from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.mappers.fetch_options_mappers import FetchOptionsMapper
from apps.scavenger.services.FilterTypeDictionary import FilterTypeDictionary
from datasource import DbLikeDataSource


class FilterFetcher:
    data_source: DbLikeDataSource = None

    def __init__(self, data_source: DbLikeDataSource):
        self.data_source = data_source

    def fetch(self):
        session: Session = self.data_source.open_session()

        statement = select(FetchOptionsTable).where(FetchOptionsTable.is_active)
        res: Sequence[Row[FetchOptionsTable]] = session.execute(statement).unique()

        fetch_options = self._process(res)

        session.close()

        return fetch_options

    def _process(self, result: Sequence[Row[FetchOptionsTable]]) -> List[FetchOptions]:
        return list(
            map(
                lambda item: FetchOptionsMapper(FilterTypeDictionary(self.data_source)).from_entity(item[0]),
                result
            )
        )
