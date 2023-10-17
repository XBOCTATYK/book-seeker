from sqlalchemy import Integer, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class OffsetPointerDto(BaseDto):
    __tablename__ = 'offset_pointer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    key: Mapped[str] = mapped_column(String(length=64), unique=True)
    value: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean)

    def get_table(self):
        return self.__table__
