from dataclasses import dataclass

from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from apps.analyser.model.CleanDataParamDto import CleanDataParamDto
from common.model.db.BaseDto import BaseDto


@dataclass
class CleanDataDto(BaseDto):
    __tablename__ = 'clean_data'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    param_set: Mapped[List[CleanDataParamDto]] = relationship(lazy=False)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    def __str__(self):
        return f"id={self.id}, param_set={self.param_set}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at}"

