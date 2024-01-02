from typing import Callable, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.event_bus.model.db.MessageDto import MessageDto
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class EventRepository(AbstractRepository):
    _offset_repository: OffsetPointerRepository
    _data_source: DbLikeDataSource

    def __init__(self, data_source: DbLikeDataSource, offset_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._offset_repository = offset_repository
        self._data_source = data_source

    def process_next_n_new_events(self, amount: int) -> list[MessageDto]:
        return self.call_in_transaction(
            lambda sess: self._offset_repository.call_in_window(
                10,
                lambda bottom, top: self._process_next_n_new_events(sess, bottom, top, lambda messages: messages)
            )
        )

    def _process_next_n_new_events(self, sess: Session, bottom: int, top: int, fn: Callable[[list[MessageDto]], Any]) -> list[MessageDto]:
        select_statement = select(MessageDto).where(MessageDto.id > bottom, MessageDto.id < top)
        res = list(sess.execute(select_statement).scalars().all())

        fn(res)

        return res


