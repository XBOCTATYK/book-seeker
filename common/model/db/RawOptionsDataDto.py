from DateTime import DateTime
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON

from common.lib.to_str import to_str
from common.model.db.BaseDto import BaseDto


@to_str
class RawOptionsDataDto(BaseDto):
    __tablename__ = "rawdata"

    id: int = Column(BigInteger, primary_key=True)
    raw_data: str = Column(JSON)
    writer: str = Column(String)
    datetime: str = Column(TIMESTAMP(timezone=True), default=DateTime().ISO())
