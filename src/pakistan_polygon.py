import geojson
import pickle
from shapely.geometry import Point, Polygon

path_ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/boundaries/polygon/countries.geojson"
path__ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/boundaries/polygon/pak_polygon"


def load_polygon(path: str = path__) -> Polygon:

    if path.find('geojson') != -1:
        with open(path) as f:
            geo = geojson.load(f)

        pak = geo["features"][174]
        pol = []
        for i in pak["geometry"]["coordinates"]:
            points = []

            for j in i[0]:
                points.append(Point(j[0], j[1]))

            pol.append(points)

        # point1 = pol[0]
        # poly1 = Polygon([[p.x, p.y] for p in point1])

        point2 = pol[1]
        pak_polygon = Polygon([[p.x, p.y] for p in point2])

    else:
        # Load polygon from disc
        with open(path, "rb") as poly_file:
            pak_polygon = pickle.load(poly_file)

    return pak_polygon
