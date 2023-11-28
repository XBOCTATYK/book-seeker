from multiprocessing import Process

from apps.analyser.AnalyzerApp import AnalyzerApp
from apps.notifier.NotifierApp import NotifierApp
from apps.raw_fetch_options_processor.RawFetchOptionsProcessorApp import RawFetchOptionsProcessorApp
from apps.scavenger.ScavengerApp import ScavengerApp
from common.db_migrations.CommonMigrationScheme import CommonMigrationScheme
from configlib.ConfigService import ConfigService
from configlib.formatters.DbConfigFormatter import DbConfigFormatter
from configlib.formatters.JsonConfigFormatter import JsonConfigFormatter
from apps.db_migrations.BookAppsMigrations import BookAppsMigrations
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider
import sys


def run_scavenger(config: dict):
    ScavengerApp(config).start()


def run_analyser(config: dict):
    AnalyzerApp(config).start()


def run_raw_fetch_options_processor(config: dict):
    RawFetchOptionsProcessorApp(config).start()


def run_notifier(config: dict):
    NotifierApp(config).start()


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

    print('Got config', config_service.config())

    p1 = Process(target=run_scavenger, args=[config])
    p2 = Process(target=run_analyser, args=[config])
    p3 = Process(target=run_raw_fetch_options_processor, args=[config])
    p4 = Process(target=run_raw_fetch_options_processor, args=[config])
    #
    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    #
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()

    migration_flag = sys.argv[1] == '-m'

    if migration_flag:
        print('Migration started!')

        db_migrations_schemes = list(map(
            lambda app: app.migrations()(),
            [NotifierApp]
        ))

        BookAppsMigrations(
            data_source,
            db_config,
            [CommonMigrationScheme()] + db_migrations_schemes
        ).start()
