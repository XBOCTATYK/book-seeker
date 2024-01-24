from apps.AbstractApp import AbstractApp
from apps.features.db_migrations.FeaturesAppMigrationScheme import FeatureAppMigrationScheme
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme


class FeaturesApp(AbstractApp):
    _config = {}

    def __init__(self, config: dict):
        super().__init__(config)
        self._config = config

    def start(self):
        pass

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    def start_migrations(self) -> AbstractMigrationScheme:
        return FeatureAppMigrationScheme()
