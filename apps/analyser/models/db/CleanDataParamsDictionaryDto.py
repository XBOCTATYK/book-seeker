from dataclasses import dataclass

from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@dataclass
@to_str
class CleanDataParamsDictionaryDto(BaseDto):
    __tablename__ = 'clean_data_params_dictionary'

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(512), unique=True, index=True)

    def __str__(self):
        return f"id={self.id}, name={self.name}"
