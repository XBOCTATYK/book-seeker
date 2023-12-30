from sqlalchemy import Enum


class EUserState(Enum):
    INITIAL = 'INITIAL'
    FETCHING = 'FETCHING'
    FETCHED = 'FETCHED'
    STATISTIC = 'STATISTIC'
