from shapely.geometry import Point, Polygon
from pyproj import Transformer
from shapely.ops import transform
from functools import partial
import pyproj
from math import radians, cos, sin, asin, sqrt, atan2, degrees


def haversine_distance(lon1: float, lon2: float, lat1: float, lat2: float) -> tuple[float, float]:
    """
    Calculate the great circle distance between two points (in nautical miles) and bearing
    on the earth (specified in decimal degrees)
    """

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    area = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    circumference = 2 * asin(sqrt(area))

    radius_in_kms = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    # km = circumference * radius
    # km_to_conv_fac = 0.621371
    # nautical_miles = km * km_to_conv_fac
    nautical_miles = circumference * radius_in_kms * 0.621371

    bearing = atan2(sin(lon2 - lon1) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    return nautical_miles, bearing


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


def geodesic_point_buffer(center: Point | Polygon, radius_in_meters: float = 1200):
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

    # Azimuthal equidistant projection

    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=center.y, lon=center.x)),
        proj_wgs84)

    if radius_in_meters == 0:
        buf = Point(0, 0).buffer(0.00000000001)
        return transform(project, buf)

    buf = Point(0, 0).buffer(radius_in_meters)  # distance in metres
    return transform(project, buf)
