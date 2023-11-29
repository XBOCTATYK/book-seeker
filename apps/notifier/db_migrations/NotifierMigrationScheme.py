from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.notifier.models.db.TgUserDto import TgUserDto
from apps.notifier.models.db.TgUserToFetchOptions import TgUserToFetchOptions
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class NotifierMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            TgUserDto,
            TgUserToFetchOptions,
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass