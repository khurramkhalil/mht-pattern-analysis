from typing import Optional
import pandas as pd
from shapely.geometry import Point
from dataclasses import dataclass

path_ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/friendly/friendly-VPs/vps.csv"


@dataclass
class VitalPoints:
    lon: float
    lat: float
    name: str
    priority: int
    size: Optional[float]

    def __post_init__(self):
        self.address: Point
        self.address = Point(self.lon, self.lat)

    def distance_from_IB(self):
        pass


def vital_points(path: str = path_) -> list[VitalPoints]:
    try:
        vps = pd.read_csv(path)
        return [VitalPoints(*vp.tolist()) for vp in vps.to_numpy()]

    except FileNotFoundError:
        print("Wrong file or file path")


x = vital_points()

# x = VitalPoints(38, 73, 'base', 38, 10)
