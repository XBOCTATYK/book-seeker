from dataclasses import dataclass

from DateTime import DateTime

from apps.scavenger.models.logic.FilterOptions import FilterOptions
from apps.scavenger.models.logic.MapViewBox import MapViewBox


@dataclass
class FetchOptions:
    map_box: MapViewBox
    checkout: DateTime
    checkin: DateTime
    filter: FilterOptions
    currency: str
