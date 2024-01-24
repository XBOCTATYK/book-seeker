from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class ConditionTypeDto(BaseDto):
    __tablename__ = 'condition_types'

    condition_type_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    condition_type_name: Mapped[str] = mapped_column(String(63), unique=True, nullable=False)
    condition_type_desc: Mapped[str] = mapped_column(String(255), nullable=False)
