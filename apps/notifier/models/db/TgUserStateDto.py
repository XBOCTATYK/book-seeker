from DateTime import DateTime
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from apps.notifier.models.db.TgUserDto import TgUserDto
from apps.notifier.models.enums.EUserState import EUserState
from common.lib import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class TgUserStateDto(BaseDto):
    __tablename__ = 'tg_user_state'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey(TgUserDto.tg_id))
    state: Mapped[str] = mapped_column(String(32), default=EUserState.INITIAL)
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
