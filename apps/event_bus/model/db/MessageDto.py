from dataclasses import dataclass
from typing import Optional

from DateTime import DateTime
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON
from sqlalchemy.orm import Mapped, mapped_column

from apps.event_bus.model.db.TopicDto import TopicDto
from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@dataclass
@to_str
class MessageDto(BaseDto):
    __tablename__ = 'message'

    id: Optional[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    text: str = mapped_column(JSON, default={'type': 'empty'})
    topic: str = mapped_column(ForeignKey(TopicDto.id))
    created_at: str = mapped_column(TIMESTAMP(timezone=True), default=DateTime().ISO())
