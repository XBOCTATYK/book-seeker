from typing import List, Callable, Type

from sqlalchemy import Connection

from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.AppConfigDto import AppConfigDto
from common.model.db.BaseDto import BaseDto
from common.model.db.OffsetPointerDto import OffsetPointerDto


class CommonMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            AppConfigDto,
            OffsetPointerDto,
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass
