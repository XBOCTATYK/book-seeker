from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.notifier.models.db.TgUserDto import TgUserDto
from common.services.AbstractRepository import AbstractRepository


class TgUserRepository(AbstractRepository):
    def get_all_active(self):
        return self._get_all_active(self._get_current_session())

    def _get_all_active(self, sess: Session) -> list[TgUserDto]:
        statement = select(TgUserDto).where(TgUserDto.is_active == True)
        result = sess.execute(statement).scalars().all()

        return list(result)

