from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class ConditionOperatorsDto(BaseDto):
    __tablename__ = 'condition_operators'

    operator_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    operator_name: Mapped[str] = mapped_column(String(31), nullable=False)
    operator_desc: Mapped[str] = mapped_column(String(255), nullable=False)