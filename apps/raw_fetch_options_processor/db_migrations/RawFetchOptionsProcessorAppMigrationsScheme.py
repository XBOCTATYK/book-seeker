from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.raw_fetch_options_processor.model.db.RawFetchOptionsDto import RawFetchOptionsDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class RawFetchOptionsProcessorAppMigrationsScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            RawFetchOptionsDto
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass
