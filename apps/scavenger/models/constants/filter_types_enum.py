from enum import Enum

from apps.scavenger.models.constants.filter_enums import EPaymentDetails, ERoomFacility, EHotelFacility


class EFilterType(Enum):
    REVIEW_SCORE = 'review_score',
    ROOMS = 'rooms',
    ONLY_AVAILABLE = 'oos',
    MIN_PRICE = 'min_price',
    MAX_PRICE = 'max_price',
    CURRENCY = 'currency',
    DISTANCE = 'distance',
    ROOMS_COUNT = 'entire_place_bedroom_count',
    FREE_CANCELLATION = f"{EPaymentDetails.get_prefix()}={EPaymentDetails.FREE_CANCELLATION.value}",
    WITHOUT_CARD = f"{EPaymentDetails.get_prefix()}={EPaymentDetails.WITHOUT_CARD.value}",
    NO_PREPAYMENT = f"{EPaymentDetails.get_prefix()}={EPaymentDetails.NO_PREPAYMENT.value}",
    AIR_COND = f"{ERoomFacility.get_prefix()}={ERoomFacility.AIR_COND.value}",
    PRIVATE_BATHROOM = f"{ERoomFacility.get_prefix()}={ERoomFacility.BATHROOM.value}",
    FREE_WIFI = f"{EHotelFacility.get_prefix()}={EHotelFacility.FREE_WIFI.value}",
    SOMETHING = f"{EHotelFacility.get_prefix()}={EHotelFacility.SOMETHING.value}",

    @classmethod
    def values(cls):
        return list(map(lambda val: val.value[0], cls._member_map_.values()))
