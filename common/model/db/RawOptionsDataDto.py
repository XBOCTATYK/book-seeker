from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON

from common.model.db.BaseDto import BaseDto


class RawOptionsDataDto(BaseDto):
    __tablename__ = "rawdata"

    id: int = Column(BigInteger, primary_key=True)
    raw_data: str = Column(JSON)
    writer: str = Column(String)
    datetime: str = Column(TIMESTAMP(timezone=True))
