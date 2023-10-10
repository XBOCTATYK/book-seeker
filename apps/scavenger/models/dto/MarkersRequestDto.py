from typing import TypedDict


class MarkerRequestParamsDto:
    class QueryParams(TypedDict):
        dest_type: str
        ref: str
        limit: int
        lang: int
        checkin: str
        checkout: str
        room1: str
        maps_opened: str
        sr_countrycode: str
        spr: str  # show prices
        nor: str # number of reviews
        sech: str # discount info
        currency: str
        nflt: str  # filters
        order: str  # popularity
        ltfd_excl: str  # map box

    class Headers(TypedDict):
        authority: str
        accept: str
        accept_language: str
        cookie: str
        referer: str
        sec_ch_ua: str
        sec_fetch_mode: str
        sec_fetch_site: str
        sec_gpc: str
        user_agent: str
