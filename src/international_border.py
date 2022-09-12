from typing import Optional
import geojson  # type: ignore

# Path to the file
path_ = "C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/boundaries/vision_crs/international_border.geojson"

# Bounds of Pakistan border.
bounds = [9, 8,  # LoC (Kashmir) + Entire boundary of Pakistan minus sea boundaries and AJ&K
          # 21, 22, 25, 26, 27, 30, 33, 35, 36, 55, 106, 107, 110, 111, 191,
          # 265, 267, 268, 269, 270, 271, 273, 274, 276,  # Sea boundaries (all remaining entries)
          ]


def load_boundaries(bound: Optional[list] = None, path: str = path_) -> list[list[float | None, float | None]]:

    sea_bound = []
    if bound is None:
        bound = bounds
        sea_bound = [[68.191731, 23.729872], [66.685037, 24.996638], [64.612992, 25.206883], [61.62981, 25.226044],
                     [None, None]]

    try:
        # Open and load geojson file
        with open(path) as f:
            pak_geo_dataframe = geojson.load(f)

    except FileNotFoundError:
        print("Wrong file or file path")

    boundary = []
    for i in bound:
        line = pak_geo_dataframe["features"][i].geometry.coordinates[0]

        if i == 7:
            # End of IOK boundary
            line = line[:252]
        if i == 191:
            # End of Pakistan boundaries at sea
            line = line[:1600]

        line.append([None, None])

        boundary.append(line)

    if sea_bound:
        boundary.insert(1, sea_bound)

    return [item for sublist in boundary for item in sublist]
