from typing import Optional
import pandas as pd
from shapely.geometry import Point
from dataclasses import dataclass
from src.geom_calculations import dynamic_range

path_ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/friendly/friendly-ground/gbads.csv"


@dataclass
class GroundAssets:
    lon: float
    lat: float
    name: str
    range_: float
    salvo: Optional[float]

    def address(self):
        return Point(self.lon, self.lat)

    def get_range(self):
        # self.range_ = 1
        return dynamic_range(self.address(), self.range_ * 1600)

    # def __post_init__(self):
    #     self.range_ = 1
    #     self.kill_zone, self.poly_circle = dynamic_range(self.address(), self.range_ * 400)


def ground_assets(path: str = path_) -> list[GroundAssets]:
    try:
        vps = pd.read_csv(path)
        return [GroundAssets(*vp.tolist()) for vp in vps.to_numpy()]

    except FileNotFoundError:
        print("Wrong file or file path")
