from dataclasses import dataclass

from apps.scavenger.models.logic.Coordinate import Coordinate
from common.lib.to_str import to_str


@dataclass
@to_str
class MapViewBox:
    top_left: Coordinate
    bottom_right: Coordinate
