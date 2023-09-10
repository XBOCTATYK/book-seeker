from dataclasses import dataclass

from apps.scavenger.models.logic.Coordinate import Coordinate


@dataclass
class MapViewBox:
    top_left: Coordinate
    bottom_right: Coordinate
