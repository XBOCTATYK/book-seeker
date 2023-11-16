from typing import List, Type, Callable

from apps.analyser.db_migrations.ParamWeightMigration import insert_weights
from apps.analyser.db_migrations.dictionaries import migration_dictionaries
from apps.analyser.models.db.CleanDataDto import CleanDataDto
from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from apps.analyser.models.db.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from apps.analyser.models.db.ParamWeightDto import ParamWeightDto
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.model.db.BaseDto import BaseDto


class AnalyserAppMigrationScheme(AbstractMigrationScheme):
    def get_tables(self) -> List[Type[BaseDto]]:
        return [
            CleanDataDto,
            CleanDataParamDto,
            CleanDataParamsDictionaryDto,
            ParamWeightDto,
        ]

    def get_dictionaries(self) -> dict[str, List[str]]:
        return migration_dictionaries

    def fill_with_data(self) -> List[Callable]:
        return [insert_weights]
