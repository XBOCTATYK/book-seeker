from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON

from common.model.db.BaseDto import BaseDto


class RawOptionsDataDto(BaseDto):
    __tablename__ = "rawdata"

    id: int = Column(Integer, primary_key=True)
    raw_data: str = Column(JSON)
    writer: str = Column(String)
    datetime: DateTime = Column(TIMESTAMP(timezone=True))
