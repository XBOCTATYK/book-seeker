from typing import List, Callable, Type

from sqlalchemy import Connection

from apps.scavenger.models.db.FetchOptionsTable import FetchOptionsTable
from apps.scavenger.models.db.FilterOptionsTable import FilterOptionsTable
from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto
from apps.scavenger.models.db.RawOptionsDataDto import RawOptionsDataDto

scavenger_app_dictionaries = {
    'filter_types': [
        'review_score',
        'rooms',
        'oos',
        'min_price',
        'max_price',
        'currency'
    ]
}


class ScavengerAppMigrationsScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            RawOptionsDataDto,
            FetchOptionsTable,
            FilterOptionsTable,
            FilterTypesTable,
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return scavenger_app_dictionaries

    def fill_with_data(self) -> List[Callable[[Connection], any]]:
        pass
