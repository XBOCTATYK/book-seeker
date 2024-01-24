from DateTime import DateTime
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from apps.analyser.models.db.CleanDataDto import CleanDataDto
from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class FilteredResultDto(BaseDto):
    __tablename__ = 'filtered_results'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    param_set: Mapped[int] = mapped_column(ForeignKey(CleanDataDto.id))
    clean_data: Mapped[CleanDataDto] = relationship(lazy=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
