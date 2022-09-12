import pandas as pd
import numpy as np
from utils import haversine_distance

target_data = pd.read_csv("D:/Khurram/tracks.csv").values[:5, :]


def insert_field(arr, val=None, heading=None):
    if heading is None:

        return np.concatenate((np.repeat(val, repeats=len(arr)).reshape(-1, 1), arr), axis=1)

    else:

        head = [haversine_distance(arr[i, -1], arr[i + 1, -1], arr[i, -2], arr[i + 1, -2])[1] for i in range(len(arr))
                if i < len(arr) - 1]
        head.insert(0, head[0])

        return np.concatenate((np.array(head).reshape(-1, 1), arr), axis=1)


def plan(arr, ids, altitude, name, priority, range_, salvo):
    flight = insert_field(np.array(arr, dtype='O'), ids)
    flight = insert_field(flight, 380)
    flight = insert_field(flight, val=None, heading=1)
    flight = insert_field(flight, altitude)
    flight = insert_field(flight, name)
    flight = insert_field(flight, priority)
    flight = insert_field(flight, range_)
    flight = insert_field(flight, salvo)

    arr = flight[:, [-3, -2, -1, -4, -5, -6, -7, -8, -9, -10]]

    return arr


plane1 = plan(target_data - 0.4, 1, 35_000, 'Su30', 210, 300, 8)
plane2 = plan(target_data - 0.2, 2, 30_000, 'Mig29', 205, 250, 4)
plane3 = plan(target_data + 0.0, 3, 40_000, 'Rafale', 215, 400, 6)
plane4 = plan(target_data + 0.2, 4, 30_000, 'Mig29', 205, 250, 4)
plane5 = plan(target_data + 0.4, 5, 35_000, 'Su30', 210, 300, 8)

planes = [plane1, plane2, plane3, plane4, plane5]
pl = [item for sublist in planes for item in sublist]

planed = [(plane1[i], plane2[i], plane3[i], plane4[i], plane5[i]) for i in range(len(plane1))]
pll = [item for sublist in planed for item in sublist]

x = pd.DataFrame(data=pll,
                 columns=['ID', 'Lon', 'Lat', 'Speed', 'Heading', 'Altitude', 'Name', 'Priority', 'Range', 'Salvo'])
# x.to_csv('targets_vstack.csv', index=False)
