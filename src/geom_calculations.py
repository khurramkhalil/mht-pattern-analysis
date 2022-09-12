import math
from typing import Any
from shapely.geometry import Polygon, Point
from rtree import index
from synthetic_data.utils import reproject_decimal_to_azimuth, geodesic_point_buffer


def dynamic_range(coordinate: Point, radius_in_meters: float = 0.25) -> tuple[list[Any], Polygon]:
    poly_circle = reproject_decimal_to_azimuth(coordinate, radius_in_meters)
    circle = list(poly_circle.exterior.coords)
    circle.append([None, None])
    return [*circle], poly_circle


def max_range(coordinate: Point | Polygon, radius_in_meters: float = 1200) -> tuple[list[tuple[float, float]],
                                                                                    list[tuple[float, float]]]:
    poly_circle = geodesic_point_buffer(coordinate, radius_in_meters)
    # circle = list(poly_circle.exterior.coords)
    # circle.append([None, None])
    # return [*circle], poly_circle
    return poly_circle


def vps_in_range(vps_idx: index, target_polygon: tuple[Polygon] | Polygon) -> list[int]:

    if isinstance(target_polygon, tuple):
        # Detect VPs that are in range of the load-out of the enemy targets
        vp_in_range = [list(vps_idx.intersection(i.bounds)) for i in target_polygon]

        # Above list may contain same VP in range of different enemy targets, get only unique VPs
        unique_vps = list(set([item for sublist in vp_in_range for item in sublist]))

    else:
        # Detect VPs that are in range of the load-out of the enemy target combine polygon and get only unique VPs
        unique_vps = list(set(vps_idx.intersection(target_polygon.bounds)))

    return unique_vps


def dynamic_arc(center: Point, start_angle: float = 210.0, end_angle: float = 330.0, radius: float = 0.25,
                steps: int = 64) -> list[tuple[float, float]]:
    def polar_point(origin_point, angle, distance):
        return [origin_point.x + math.sin(math.radians(angle)) * distance,
                origin_point.y + math.cos(math.radians(angle)) * distance]

    if start_angle > end_angle:
        start_angle = start_angle - 360.0

    else:
        pass

    step_angle_width = (end_angle - start_angle) / steps
    sector_width = (end_angle - start_angle)
    segment_vertices = [polar_point(center, 0, 0), polar_point(center, start_angle, radius)]

    for z in range(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width, radius)))

    segment_vertices.append(polar_point(center, start_angle + sector_width, radius))
    segment_vertices.append(polar_point(center, 0, 0))

    return [*Polygon(segment_vertices).exterior.coords]
