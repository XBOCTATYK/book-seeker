from apps.AbstractApp import AbstractApp
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme


class FeaturesApp(AbstractApp):
    def start(self):
        pass

    def stop(self):
        pass

    def exports(self) -> dict:
        pass

    def start_migrations(self) -> AbstractMigrationScheme:
        pass

