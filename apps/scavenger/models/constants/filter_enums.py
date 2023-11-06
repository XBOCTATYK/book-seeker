from enum import Enum


class ERoomFacility(Enum):
    AIR_COND = 11
    BATHROOM = 38

    @staticmethod
    def get_prefix():
        return 'roomfacility'


class EHotelFacility(Enum):
    FREE_WIFI = 107
    SOMETHING = 100

    @staticmethod
    def get_prefix():
        return 'hotelfacility'


class EPaymentDetails(Enum):
    FREE_CANCELLATION = 2
    WITHOUT_CARD = 4
    NO_PREPAYMENT = 5

    @staticmethod
    def get_prefix():
        return 'fc'
