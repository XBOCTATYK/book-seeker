from enum import Enum


class ERoomFacility(Enum):
    AIR_COND = 11
    BATHROOM = 38

    @classmethod
    def get_prefix(cls):
        return 'roomfacility'


class EHotelFacility(Enum):
    FREE_WIFI = 107

    @classmethod
    def get_prefix(cls):
        return 'hotelfacility'


class EPaymentDetails(Enum):
    FREE_CANCELLATION = 2,
    WITHOUT_CARD = 4,
    NO_PREPAYMENT = 5

    @classmethod
    def get_prefix(cls):
        return 'fc'
