# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 09:53:18 2022

@author: DTEAIAPPS
"""

import numpy as np
import geojson
from shapely.geometry import shape, Point, Polygon, LineString, MultiPolygon
from shapely.ops import unary_union, nearest_points
from shapely.ops import transform, split
from rtree import index
import pyproj as pyproj
from pyproj import Proj, transform
from functools import partial



import warnings
warnings.filterwarnings("ignore")

path = "D:/Khurram/countries.geojson"

with open(path) as f:
    geo  = geojson.load(f)

#  Pakistan is at i = 174
# for i in range(len(geo["features"])):
#     line = geo["features"][i]["properties"]["ADMIN"]
#     # print(line)
    
#     if line == "Pakistan":
#         pak = geo["features"][i]
#         break

# pol = []
# for i in pak["geometry"]["coordinates"]:
#     points = []
    
#     for j in i[0]:
#         # print(j)
#         points.append(Point(j[0], j[1]))
    
#     pol.append(points)



pol = []
for i in geo["features"][174]["geometry"]["coordinates"]:
    points = []
    
    for j in i[0]:
        # print(j)
        points.append(Point(j[0], j[1]))
    
    pol.append(points)


# point1 = pol[0]
# poly1 = Polygon([[p.x, p.y] for p in point1])

pak_poly = pol[1]


# pak = Proj(pak_poly)

pak_poly = Polygon([[p.x, p.y] for p in pak_poly])

# pak_poly1 = MultiPolygon([[p] for p in pak_poly])

p1 = Point([73.9567317, 33.843616])
p2 = Point([74.262425, 33.999103])

# Nearest point
a, b = nearest_points(pak_poly, p2)


# idx = index.Index()
# for pos, poly in enumerate(pak["geometry"]["coordinates"]):
#       idx.insert(pos, shape(poly).bounds)


from math import radians, cos, sin, asin, sqrt, atan2, degrees

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    km = c * r
    km_to_conv_fac = 0.621371
    nautical_miles = km * km_to_conv_fac
    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    
    return nautical_miles, bearing


# km, bearing = haversine(s.x, s.y, s2.x, s2.y)
# km, bearing = haversine(s2.x, s2.y, s.x, s.y)



x = p1.buffer(0.25)


for a, b in x.exterior.coords:
    print(a,b)






def __geodesic_point_buffer(self, lon, lat, km):
        """
        Based on: https://gis.stackexchange.com/questions/289044/creating-buffer-circle-x-kilometers-from-point-using-python

        Args:
            lon:
            lat:
            km:

        Returns:
            a list of coordinates with radius km and center (lat,long) in this projection
        """
        proj_wgs84 = pyproj.Proj(init='epsg:4326')
        # Azimuthal equidistant projection
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
            proj_wgs84)
        buf = Point(0, 0).buffer(km * 1000)  # distance in metres
        return transform(project, buf).exterior.coords[:] 























