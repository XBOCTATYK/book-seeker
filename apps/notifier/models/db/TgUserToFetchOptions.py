from typing import List

from DateTime import DateTime
from sqlalchemy import BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from common.model.db.BaseDto import BaseDto


class TgUserToFetchOptions(BaseDto):
    __tablename__ = 'tg_user_to_fetch_options'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    # TODO: extract to separate table
    tg_user: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    fetch_options: Mapped[List['FetchOptionsTable']] = relationship(lazy="select")
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
