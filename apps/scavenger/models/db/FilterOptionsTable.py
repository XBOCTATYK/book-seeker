from DateTime import DateTime
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model.db.BaseDto import BaseDto


class FilterOptionsTable(BaseDto):
    __tablename__ = 'filter_options'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    value: Mapped[str] = mapped_column(String(30))
    type: Mapped[int] = mapped_column(ForeignKey('filter_types.id'))
    fetch_options: Mapped[int] = mapped_column(ForeignKey('fetch_options.id'))
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
