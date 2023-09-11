from typing import List

from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from common.model.db.BaseDto import BaseDto


class FetchOptionsTable(BaseDto):
    __tablename__ = 'fetch_options'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    map_box: Mapped[str] = mapped_column(String(100))
    checkin: Mapped[str] = mapped_column(TIMESTAMP())
    checkout: Mapped[str] = mapped_column(TIMESTAMP())
    filters: Mapped[List['FilterOptionsTable']] = relationship(lazy=False)
    currency: Mapped[str] = mapped_column(String(4))
    is_active: Mapped[bool] = mapped_column(Boolean())
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

