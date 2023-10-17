from dataclasses import dataclass

from DateTime import DateTime
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@dataclass
@to_str
class CleanDataDto(BaseDto):
    __tablename__ = 'clean_data'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    param_set: Mapped[List['CleanDataParamDto']] = relationship(lazy=False)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())

