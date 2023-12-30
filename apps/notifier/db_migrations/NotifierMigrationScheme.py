from typing import List, Callable, Type

from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import insert

from apps.notifier.config.BotConfig import BotConfig
from apps.notifier.models.db.TgUserDto import TgUserDto
from apps.notifier.models.db.TgUserToFetchOptions import TgUserToFetchOptions
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class NotifierMigrationScheme(AbstractMigrationScheme):
    _config = {}

    def __init__(self, config: BotConfig):
        super().__init__()
        self._config = config

    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            TgUserDto,
            TgUserToFetchOptions,
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        return [self._insert_default_user]

    def _insert_default_user(self, connection: Connection):
        insert_statement = insert(TgUserDto).values([{'tg_id': self._config['user'], 'is_active': True}]) \
            .on_conflict_do_nothing()
        connection.execute(insert_statement)

        return True
