from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class FilterTypesTable(BaseDto):
    __tablename__ = 'filter_types'

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(31), unique=True)
