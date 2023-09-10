# This is a sample Python scripf
from DateTime import DateTime

from apps.scavenger.ScavengerApp import ScavengerApp
from apps.scavenger.models.logic.Coordinate import Coordinate
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox
from apps.scavenger.services.BookDataFetcher import BookDataFetcher
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

    ScavengerApp(config).start()

    # data = fetcher.fetch(
    #     FetchOptions(
    #         map_box=MapViewBox(
    #             Coordinate(13.68641832626463, 100.42547080801124),
    #             Coordinate(13.759126242275268, 100.76261375234718)
    #         ),
    #         currency='RUB',
    #         checkin=DateTime('2023/10/03 UTC'),
    #         checkout=DateTime('2023/11/03 UTC'),
    #         filter=FilterOptions(
    #             rooms=1,
    #             review_score=8,
    #             oos='1',
    #             min_price=1000,
    #             max_price=4000,
    #             currency='RUB'
    #         )
    #     )
    # )
    # Migrations(data_source, db_config).start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
