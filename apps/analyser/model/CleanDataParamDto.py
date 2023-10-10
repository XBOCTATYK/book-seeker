from dataclasses import dataclass

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.model.db.BaseDto import BaseDto


@dataclass
class CleanDataParamDto(BaseDto):
    __tablename__ = 'clean_data_param'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    param_set: Mapped[int] = mapped_column(ForeignKey('clean_data.id'))
    type: Mapped[int] = mapped_column(ForeignKey('clean_data_params_dictionary.sql.id'))
    value: Mapped[str] = mapped_column(String(length=512))

    def __str__(self):
        return f"id={self.id}, param_set={self.param_set}, type={self.type}, value={self.value}"
