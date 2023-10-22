from sqlalchemy.orm import DeclarativeBase


class BaseDto(DeclarativeBase):
    id: int = None

    pass
