from DateTime import DateTime
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from apps.event_bus.model.db.TopicDto import TopicDto
from common.model.db.BaseDto import BaseDto


class MessageDto(BaseDto):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255))
    topic: Mapped[str] = mapped_column(ForeignKey(TopicDto.id))
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
