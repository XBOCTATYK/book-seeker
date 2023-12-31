from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.event_bus.model.db.MessageDto import MessageDto
from apps.event_bus.model.db.TopicDto import TopicDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class EventBusAppMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            TopicDto,
            MessageDto
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass

