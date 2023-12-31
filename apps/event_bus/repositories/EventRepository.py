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

    def get_next_n_new_events(self, amount: int) -> list[MessageDto]:
        return self.call_in_transaction(
            lambda sess: self._offset_repository.call_in_window(
                amount,
                lambda bottom, top: self._get_next_n_events(sess, bottom, top)
            )
        )

    def process_next_n_new_events(self, amount: int) -> list[MessageDto]:
        return self.call_in_transaction(
            lambda sess: self._offset_repository.call_in_window(
                amount,
                lambda bottom, top: self._process_next_n_new_events(sess, bottom, top, lambda messages: messages)
            )
        )

    def save(self, value: MessageDto):
        self.call_in_transaction(lambda sess: self._save(sess, value))

    @staticmethod
    def _save(sess: Session, message: MessageDto):
        sess.add(message)
        sess.flush([message])

    @staticmethod
    def _get_next_n_events(sess, bottom, top) -> list[MessageDto]:
        select_statement = select(MessageDto).where(MessageDto.id > bottom, MessageDto.id < top)
        return list(sess.execute(select_statement).scalars().all())

    @staticmethod
    def _process_next_n_new_events(
            sess: Session,
            bottom: int,
            top: int,
            fn: Callable[[list[MessageDto]], Any]
    ) -> list[MessageDto]:
        res = EventRepository._get_next_n_events(sess, bottom, top)

        fn(res)

        return res
