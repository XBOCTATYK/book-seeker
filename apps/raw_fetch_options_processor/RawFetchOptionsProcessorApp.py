from apps.AbstractApp import AbstractApp
from apps.raw_fetch_options_processor.db_migrations.RawFetchOptionsProcessorAppMigrationsScheme import \
    RawFetchOptionsProcessorAppMigrationsScheme


class RawFetchOptionsProcessorApp(AbstractApp):
    def start(self):
        pass

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    @staticmethod
    def migrations():
        return RawFetchOptionsProcessorAppMigrationsScheme
