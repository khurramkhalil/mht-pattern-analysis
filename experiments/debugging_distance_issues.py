# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:42:31 2022

@author: DTEAIAPPS
"""


import numpy as np
import geojson
from shapely.geometry import shape, Point, Polygon, LineString, MultiPolygon
from shapely.ops import unary_union, nearest_points
from shapely.ops import transform, split
from rtree import index
import pyproj as pyproj
from pyproj import Proj, Transformer
from functools import partial
from pyproj import Transformer


import warnings
warnings.filterwarnings("ignore")

path = "D:/Khurram/countries.geojson"


def reproject_decimal_to_azimuth(center: Point, radius_in_meters: float = 1000):
    # Enter in following order .format(latitude, longitude)
    local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(center.y, center.x)
    wgs84_to_aeqd = Transformer.from_proj('+proj=longlat +datum=WGS84 +no_defs', local_azimuthal_projection)
    aeqd_to_wgs84 = Transformer.from_proj(local_azimuthal_projection, '+proj=longlat +datum=WGS84 +no_defs')

    # Get polygon with lat lon coordinates. Enter .transform(longitude, latitude)
    point_transformed = Point(wgs84_to_aeqd.transform(center.x, center.y))

    buffer = point_transformed.buffer(radius_in_meters)
    circle = transform(aeqd_to_wgs84.transform, buffer)

    return circle

def geodesic_point_buffer(center: Point, radius_in_meters: float = 1200):
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

    # Azimuthal equidistant projection

    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=center.y, lon=center.x)),
        proj_wgs84)

    # if radius_in_meters == 0:
    #     buf = Point(0, 0).buffer(0.00000000001)
    #     return transform(project, buf)

    buf = Point(0, 0).buffer(radius_in_meters)  # distance in metres
    return transform(project, buf)

# .exterior.coords[:]

def dynamic_range(coordinate: Point, radius_in_meters: float = 1200) -> tuple[list[tuple[float, float]],
                                                                              list[tuple[float, float]]]:
    poly_circle = reproject_decimal_to_azimuth(coordinate, radius_in_meters)
    # poly_circle = geodesic_point_buffer(coordinate, radius_in_meters)
    circle = list(poly_circle.exterior.coords)
    circle.append([None, None])
    return [*circle], poly_circle



with open(path) as f:
    geo  = geojson.load(f)


pol = []
for i in geo["features"][174]["geometry"]["coordinates"]:
    points = []
    
    for j in i[0]:
        # print(j)
        points.append(Point(j[0], j[1]))
    
    pol.append(points)


pak_poly = pol[1]


pak_poly = Polygon([[p.x, p.y] for p in pak_poly])


p1 = Point([73.9567317, 33.843616])
p2 = Point([74.262425, 33.999103])

# Nearest point
a, b = nearest_points(pak_poly, p2)

lahore = Point(74.483592, 31.389204)

gbad, gg = dynamic_range(lahore, 120000)

waga = Point(74.627209, 31.506264)
test = Point(75.65746189999996, 30.53771275000001)































