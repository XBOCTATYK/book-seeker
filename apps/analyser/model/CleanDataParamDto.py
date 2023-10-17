from dataclasses import dataclass

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from apps.analyser.model.CleanDataDto import CleanDataDto
from apps.analyser.model.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@dataclass
@to_str
class CleanDataParamDto(BaseDto):
    __tablename__ = 'clean_data_param'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    param_set: Mapped[int] = mapped_column(ForeignKey(CleanDataDto.id))
    type: Mapped[int] = mapped_column(ForeignKey(CleanDataParamsDictionaryDto.id))
    value: Mapped[str] = mapped_column(String(length=512))
