from sqlalchemy import SmallInteger, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class UserConditionsDto(BaseDto):
    __tablename__ = 'user_conditions'

    user_condition_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    condition_id: Mapped[int] = mapped_column(ForeignKey('feature_conditions.condition_id'))
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
