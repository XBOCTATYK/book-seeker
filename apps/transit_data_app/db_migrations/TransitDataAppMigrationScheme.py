from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class TransitDataAppMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            FilteredResultDto
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass
