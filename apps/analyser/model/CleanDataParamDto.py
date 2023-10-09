from dataclasses import dataclass

from sqlalchemy import BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.model.db.BaseDto import BaseDto


@dataclass
class CleanDataParamDto(BaseDto):
    __tablename__ = 'clean_data_param'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True)
    param_set: Mapped[int] = mapped_column(ForeignKey('clean_data.id'))
    type: Mapped[int] = mapped_column(ForeignKey('clean_data_params_dictionary.id'))
    value: Mapped[str] = mapped_column(String(length=512))
