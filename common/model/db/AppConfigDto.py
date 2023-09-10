from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP

from common.model.db.BaseDto import BaseDto


class AppConfigDto(BaseDto):
    __tablename__ = "app_config"

    id: int = Column(Integer, primary_key=True)
    key: str = Column(String)
    value: str = Column(String)
    is_active: bool = Column(Boolean)
    created_at: str = Column(TIMESTAMP(timezone=True))
    updated_at: str = Column(TIMESTAMP(timezone=True))
