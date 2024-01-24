from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class FeatureDto(BaseDto):
    __tablename__ = 'features'

    feature_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True, unique=True)
    feature_name: Mapped[str] = mapped_column(String(63), unique=True, nullable=False)
    feature_desc: Mapped[str] = mapped_column(String(255), nullable=False)
