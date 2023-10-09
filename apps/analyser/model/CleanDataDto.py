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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True)
    param_set: Mapped[List[CleanDataParamDto]] = relationship(lazy=False)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

