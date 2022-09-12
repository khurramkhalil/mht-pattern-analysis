from typing import Generator
import pandas as pd
import numpy as np
from shapely.geometry import Point
from dataclasses import dataclass
from src.geom_calculations import dynamic_range

path_ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/enemy/enemy-airborne/targets_vstack.csv"


@dataclass
class AirborneTargets:
    ID: int
    lon: float
    lat: float
    speed: float
    heading: float
    altitude: float
    name: str
    priority: int
    range_: float
    salvo: int

    def address(self):
        return Point(self.lon, self.lat)

    def get_range(self):
        # self.range_ = 1
        return dynamic_range(self.address(), self.range_ * 300)

    # def __post_init__(self):
    #     self.range_ = 1
    #     self.max_range, self.poly_circle = dynamic_range(self.address(), self.range_ * 1200)


def make_tracks(tracks: np.ndarray) -> list[AirborneTargets]:
    try:
        return [AirborneTargets(*track.tolist()) for track in tracks]

    except FileNotFoundError:
        print("Wrong file or file path")


def airborne_targets(path: str = path_) -> Generator[list[AirborneTargets], None, None]:
    try:
        airborne = pd.read_csv(path).values
        all_tracks = (make_tracks(airborne[track:track + 5, :]) for track in range(0, len(airborne), 5))
        return all_tracks

    except FileNotFoundError:
        print("Wrong file or file path")


if __name__ == "__main__":
    x = airborne_targets()
