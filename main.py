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


def run_scavenger(scavenger_config: dict):
    ScavengerApp(scavenger_config).start()


def run_analyser(analyser_config: dict):
    AnalyzerApp(analyser_config).start()


def run_raw_fetch_options_processor(rafo_config: dict):
    RawFetchOptionsProcessorApp(rafo_config).start()


def run_notifier(notifier_config: dict):
    NotifierApp(notifier_config).start()


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
    print(sys.argv)
    migration_flag = sys.argv[1] == '-m' if len(sys.argv) > 1 else False

    if migration_flag:
        print('Migration started!')

        db_migrations_schemes = list(map(
            lambda app: app.start_migrations(),
            [NotifierApp(config), ScavengerApp(config), AnalyzerApp(config), RawFetchOptionsProcessorApp(config)]
        ))

        BookAppsMigrations(
            data_source,
            db_config,
            [CommonMigrationScheme()] + db_migrations_schemes
        ).start()

    p1 = Process(target=run_scavenger, args=[config])
    p2 = Process(target=run_analyser, args=[config])
    p3 = Process(target=run_raw_fetch_options_processor, args=[config])
    p4 = Process(target=run_notifier, args=[config])
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()


