from dataclasses import dataclass
from typing import TypedDict

from DateTime import DateTime

from apps.scavenger.models.logic.MapViewBox import MapViewBox


class FetchOptions(TypedDict):
    map_box: MapViewBox
    checkin: DateTime
    checkout: DateTime
    filter: dict
    currency: str
    persons: int
