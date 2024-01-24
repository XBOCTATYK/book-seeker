from sqlalchemy import SmallInteger, Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class ListConditionsDto(BaseDto):
    __tablename__ = 'list_items'

    list_item_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    list_item_value: Mapped[str] = mapped_column(String(255), nullable=False)
    condition_id: Mapped[int] = mapped_column(ForeignKey('feature_conditions.condition_id'))
