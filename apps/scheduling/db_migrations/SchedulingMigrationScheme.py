from typing import List, Type, Callable

from sqlalchemy import Connection

from apps.scheduling.models.db.SchedulerWorkTimeDto import SchedulerWorkTimeDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class SchedulingMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            SchedulerWorkTimeDto
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return {}

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass
