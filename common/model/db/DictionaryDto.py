from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from common.model.db.BaseDto import BaseDto


class DictionaryDto(BaseDto):
    __tablename__ = 'dicts'

    id: Mapped[int] = mapped_column(Integer, unique=True, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String)

