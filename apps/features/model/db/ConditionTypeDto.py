from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class ConditionTypeDto(BaseDto):
    __tablename__ = 'condition_types'

    condition_type_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    condition_type_name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    condition_type_desc: Mapped[str] = mapped_column(String(255), nullable=False)
