from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class FeatureDto(BaseDto):
    __tablename__ = 'features'

    feature_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True, unique=True)
    feature_name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    feature_desc: Mapped[str] = mapped_column(String(255), nullable=False)
