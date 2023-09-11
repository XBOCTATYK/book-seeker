from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from common.model.db.BaseDto import BaseDto


class AppConfigDto(BaseDto):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    key: Mapped[str] = mapped_column(String, index=True)
    value: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    def get_table(self):
        return self.__table__

    def __str__(self):
        return f'id={self.id}, key={self.key}, value={self.value}, is_active={self.is_active}, created_at={self.created_at}, updated_at={self.updated_at}'
