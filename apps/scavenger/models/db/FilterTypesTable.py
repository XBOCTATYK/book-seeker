from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class FilterTypesTable(BaseDto):
    __tablename__ = 'filter_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
