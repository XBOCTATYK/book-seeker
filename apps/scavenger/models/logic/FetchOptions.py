from dataclasses import dataclass

from DateTime import DateTime

from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox


@dataclass
class FetchOptions:
    map_box: MapViewBox
    checkin: DateTime
    checkout: DateTime
    filter: FilterOptions
    currency: str
