from DateTime import DateTime
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from common.model.db.BaseDto import BaseDto


class RawFetchOptionsDto(BaseDto):
    __tablename__ = 'raw_fetch_options'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    url: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String(length=6))
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
