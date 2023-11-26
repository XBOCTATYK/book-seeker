# This is a sample Python script
from multiprocessing import Process

from apps.analyser.AnalyzerApp import AnalyzerApp
from apps.notifier.NotifierApp import NotifierApp
from apps.raw_fetch_options_processor.RawFetchOptionsProcessorApp import RawFetchOptionsProcessorApp
from apps.scavenger.ScavengerApp import ScavengerApp
from apps.scavenger.models.constants.filter_types_enum import EFilterType
from apps.scavenger.models.mappers.filter_options_mapper import FilterOptionsSerializer
from apps.scavenger.services.FilterFetcher import FilterFetcher
from apps.transit_data_app.TransitDataApp import TransitDataApp
from common.db_migrations.CommonMigrationScheme import CommonMigrationScheme
from configlib.ConfigService import ConfigService
from configlib.formatters.DbConfigFormatter import DbConfigFormatter
from configlib.formatters.JsonConfigFormatter import JsonConfigFormatter
from apps.db_migrations.BookAppsMigrations import BookAppsMigrations
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


def run_scavenger(config: dict):
    ScavengerApp(config).start()


def run_analyser(config: dict):
    AnalyzerApp(config).start()


def run_raw_fetch_options_processor(config: dict):
    RawFetchOptionsProcessorApp(config).start()


if __name__ == '__main__':
    print('Starting...')

    config_service = ConfigService(
        JsonConfigFormatter('default'),
        JsonConfigFormatter('dev'),
        JsonConfigFormatter('secret')
    )
    config = config_service.config()

    db_config = config['db']
    data_source = DbLikeDataSource(PostgresDataProvider(db_config))
    config_service.extend(DbConfigFormatter(data_source).get_config())

    print(config_service.config())

    p1 = Process(target=run_scavenger, args=[config])
    p2 = Process(target=run_analyser, args=[config])
    p3 = Process(target=run_raw_fetch_options_processor, args=[config])

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # db_migrations_schemes = list(map(
    #     lambda app: app.migrations()(),
    #     [AnalyzerApp, ScavengerApp, RawFetchOptionsProcessorApp, TransitDataApp]
    # ))
    #
    # BookAppsMigrations(
    #     data_source,
    #     db_config,
    #     [CommonMigrationScheme()] + db_migrations_schemes
    # ).start()
