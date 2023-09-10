# This is a sample Python scripf

from apps.scavenger.ScavengerApp import ScavengerApp
from configlib.ConfigService import ConfigService
from configlib.formatters.DbConfigFormatter import DbConfigFormatter
from configlib.formatters.JsonConfigFormatter import JsonConfigFormatter
from apps.db_migrations.BookAppsMigrations import BookAppsMigrations
from datasource.DbDataSource import DbDataSource
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
    data_source = DbDataSource(PostgresDataProvider(db_config))
    config_service.extend(DbConfigFormatter(data_source).get_config())

    print(config_service.config())

    ScavengerApp(config).start()

    # BookAppsMigrations(data_source, db_config).start()

