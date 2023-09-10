from apps.scavenger.models.logic.Coordinate import Coordinate
from apps.scavenger.models.logic.MapViewBox import MapViewBox


def coordinate_to_string(coordinate: Coordinate):
    return f'{coordinate.lon},{coordinate.lat}'


def map_view_box_to_string(map_view_box: MapViewBox):
    return f'{coordinate_to_string(map_view_box.top_left)},{coordinate_to_string(map_view_box.bottom_right)}'
