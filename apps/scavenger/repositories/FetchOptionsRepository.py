from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from common.services.AbstractRepository import AbstractRepository


class FetchOptionsRepository(AbstractRepository):

    def insert_values(self, values: List[dict]):
        rest = values.pop()

    def _insert_values(self, sess: Session, values: List[dict]):
        values_to_insert = list(map(lambda item: {'checkin': item['checkin'], 'checkout': item['checkout'], 'currency': item['currency']}, values))
        statement = insert(FetchOptionsTable).values(values_to_insert)