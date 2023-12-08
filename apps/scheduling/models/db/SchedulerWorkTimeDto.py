from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from common.model.db.BaseDto import BaseDto


class SchedulerWorkTimeDto(BaseDto):
    __tablename__ = 'scheduler_work_time'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    scheduler_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
