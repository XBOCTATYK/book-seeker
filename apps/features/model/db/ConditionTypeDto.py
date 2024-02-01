from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class ConditionTypeDto(BaseDto):
    __tablename__ = 'condition_types'

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(63), unique=True, nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=True)
