from sqlalchemy import BigInteger, ForeignKey, String, Boolean, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from apps.features.model.db.ConditionTypeDto import ConditionTypeDto
from apps.features.model.db.FeatureDto import FeatureDto
from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class ConditionDto(BaseDto):
    __tablename__ = 'feature_conditions'

    condition_id: int = mapped_column(BigInteger, primary_key=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey(FeatureDto.feature_id))
    condition_type_id: Mapped[int] = mapped_column(ForeignKey(ConditionTypeDto.condition_type_id))
    condition_operator: Mapped[str] = mapped_column(String(31), nullable=False)
    condition_value: Mapped[str] = mapped_column(String(31), nullable=False)
    feature_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
    chained_condition_id: Mapped[int] = mapped_column(ForeignKey('feature_conditions.condition_id'), nullable=True)
    condition_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)
