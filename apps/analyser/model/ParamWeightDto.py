from DateTime import DateTime
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from apps.analyser.model.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from common.model.db.BaseDto import BaseDto


class ParamWeightDto(BaseDto):
    __tablename__ = 'param_weights'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    param_name: Mapped[int] = mapped_column(ForeignKey(CleanDataParamsDictionaryDto.id), index=True)
    weight_value: Mapped[int] = mapped_column(Float, default=1)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
