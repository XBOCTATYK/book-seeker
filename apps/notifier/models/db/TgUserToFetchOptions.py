from DateTime import DateTime
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from apps.notifier.models.db.TgUserDto import TgUserDto
from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class TgUserToFetchOptions(BaseDto):
    __tablename__ = 'tg_user_to_fetch_options'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    tg_user: Mapped[int] = mapped_column(ForeignKey(TgUserDto.tg_id))
    fetch_options: Mapped[FetchOptionsTable] = mapped_column(ForeignKey(FetchOptionsTable.id))
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
