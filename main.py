# This is a sample Python scripf
from apps.analyser.AnalyzerApp import AnalyzerApp
from apps.notifier.NotifierApp import NotifierApp
from apps.raw_fetch_options_processor.RawFetchOptionsProcessorApp import RawFetchOptionsProcessorApp
from apps.scavenger.ScavengerApp import ScavengerApp
from apps.scavenger.models.logic.FilterOptions import FilterOptions
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

    # ScavengerApp(config).start()

    # AnalyzerApp(config).start()

    # NotifierApp(config).start()

    # TransitDataApp(config).start()

    # options = FilterFetcher(data_source).fetch()

    # options = str(FilterOptions({'review_score': 8, 'currency': 'RUB', 'max_price': 60000}))
    # print(options)
    # print(FilterOptionsSerializer().serialize(options[0].filter))

    db_migrations_schemes = list(map(
        lambda app: app.migrations()(),
        [AnalyzerApp, ScavengerApp, RawFetchOptionsProcessorApp, TransitDataApp]
    ))

    BookAppsMigrations(
        data_source,
        db_config,
        [CommonMigrationScheme()] + db_migrations_schemes
    ).start()
