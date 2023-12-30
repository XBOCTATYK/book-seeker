from DateTime import DateTime
from sqlalchemy import BigInteger, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class TgUserDto(BaseDto):
    __tablename__ = 'tg_user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
