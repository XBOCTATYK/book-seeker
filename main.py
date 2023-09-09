# This is a sample Python scripf
from configlib.ConfigService import ConfigService
from configlib.formatters.JsonConfigFormatter import JsonConfigFormatter
from apps.db_migrations.Migrations import Migrations
from datasource.DbDataSource import DbDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

    config = ConfigService(
        JsonConfigFormatter('default'),
        JsonConfigFormatter('dev'),
        JsonConfigFormatter('secret')
    ).config()

    db_config = config['db']
    data_source = DbDataSource(PostgresDataProvider(db_config))
    # Migrations(data_source, db_config).start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
