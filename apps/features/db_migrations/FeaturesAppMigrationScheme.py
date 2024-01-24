from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.analyser.db_migrations.dictionaries import migration_dictionaries
from apps.features.model.db.ConditionDto import ConditionDto
from apps.features.model.db.ConditionTypeDto import ConditionTypeDto
from apps.features.model.db.FeatureDto import FeatureDto
from apps.features.model.db.ListConditionsDto import ListConditionsDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class FeatureAppMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            FeatureDto,
            ConditionTypeDto,
            ConditionDto,
            ListConditionsDto
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return migration_dictionaries

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        return list()

