import socket
import pickle
import pandas as pd
# shape, Point, Polygon, LineString, MultiPolygon
# from shapely.strtree import STRtree
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.ops import nearest_points
from rtree import index
# from international_border import load_boundaries
from pakistan_polygon import load_polygon
from geom_calculations import max_range
from geom_calculations import vps_in_range
from synthetic_data.gbads import ground_assets
# from synthetic_data.trace_track import path_generator
from synthetic_data.vps import vital_points
from synthetic_data.airborne import airborne_targets

# Pakistan polygon
pak_polygon = load_polygon()

# DYNAMIC ITEMS
# Friendly GBADS
ground_assets = ground_assets()

gbads_idx = index.Index(properties=index.Property())
for ind, point in enumerate(ground_assets):
    gbads_idx.insert(ind, point.get_range()[1].bounds)

# Initializing polygons for GBADS (ground_assets) to be used in rtree intersection measure
ground_flat_polygon, ground_polygon = zip(*[gbad.get_range() for gbad in ground_assets])

# VP data points
vp_points = vital_points()

vps_idx = index.Index(properties=index.Property())
for ind, point in enumerate(vp_points):
    vps_idx.insert(ind, point.address.bounds)

# Calculating dynamic ranges and load-out max limits
# Calculate dynamic range of the current weapon system (declared by range_ parameter) as a circle
# gbads_kill_circle = [item for sublist in [kill.get_range()[0] for kill in ground_assets] for item in sublist]

# Getting airborne targets
all_targets = airborne_targets()


def iterate():
    # Main computation starts here.
    try:
        # Initialize empty dictionary and populate it accordingly during the course of the program
        figure = {}
        # Get updated info from tracks
        target = next(all_targets)

        figure['target'] = target
        # print(target)

        # Get polygons for enemy air targets at current instance of time to be used in rtree collision detection
        # algorithm. 'target_flat_polygon' is list of lists of lat longs with [None, None] between the targets while
        # 'target_polygon' is single polygon entity with all information enclosed within.
        target_flat_polygon, target_polygon = zip(*[tar.get_range() for tar in target])

        # Plot max_ranges of enemy air targets.
        max_range_enemy_air_targets = [item for sublist in target_flat_polygon for item in sublist]

        figure['max_range_enemy_air_targets'] = max_range_enemy_air_targets

        # Combine range of all enemy targets in polygon format
        combine_polygon = unary_union(target_polygon)
        # Get coordinates of the unified maximum single range of all enemy targets
        combine_polygon_exterior = list(combine_polygon.exterior.coords)

        figure["combine_polygon_exterior"] = combine_polygon_exterior

        # Get unique VPs that are in range of enemy targets combine polygon
        unique_vps_in_enemy_targets = vps_in_range(vps_idx, combine_polygon)
        vps = [vp_points[i] for i in range(len(vp_points)) if i in unique_vps_in_enemy_targets]
        # This gets the overlapping VPs with combine_polygon with r_tree algorithm that expects perfect square but here
        # ranges are circular. The obtained results might not be perfect. Manually verify that detected vps indeed lie
        # in the combine_polygon circle.
        vps = [vp for vp in vps if combine_polygon.contains(vp.address)]

        # Next to get the closest VP and combine_polygon of the enemy target range in given buffer area:
        # Get lat, lon coordinates from combine_polygon_exterior as shapely Point objects
        extended_combine_polygon = [Point(i[0], i[1]) for i in combine_polygon_exterior]
        # Add buffer size to each Point as given by operators (for now use 80km as test data)
        extended_combine_polygon = [max_range(i, 80000) for i in extended_combine_polygon]
        # Combine the buffered Points as single Polygon and get the exterior points of its boundary as a list
        extended_combine_polygon = unary_union(extended_combine_polygon)

        # TODO Replace rtree collision detection with shapely contains function
        # Get unique VPs that are in range of extended enemy targets combine polygon
        unique_vps_soon = vps_in_range(vps_idx, extended_combine_polygon)
        unique_vps_soon = [vp for vp in unique_vps_soon if vp not in unique_vps_in_enemy_targets]
        vps_next = [vp_points[i] for i in range(len(vp_points)) if i in unique_vps_soon]

        # Combine range of extended all enemy targets in polygon format
        extended_combine_polygon_exterior = list(extended_combine_polygon.exterior.coords)

        figure["extended_combine_polygon_exterior"] = extended_combine_polygon_exterior
        figure["vps"] = vps
        figure["vps_next"] = vps_next

        if vps_next:
            x1, x2 = zip(*[nearest_points(vp.address, combine_polygon.exterior) for vp in vps_next])
            extended_pairing_lines = []
            for i, j in zip(x1, x2):
                extended_pairing_lines.append([i.y, i.x])
                extended_pairing_lines.append([j.y, j.x])
                extended_pairing_lines.append([None, None])

            figure["extended_pairing_lines"] = extended_pairing_lines

        targets_idx = index.Index(properties=index.Property())
        targets = [track.address() for track in target]

        for edx, track in enumerate(target):
            targets_idx.insert(edx, track.address().bounds)

        if vps:

            # Straight lines between vps and closest enemy targets
            closest_target = [item for sublist in
                              [list(targets_idx.nearest(vps[i].address.bounds)) for i in range(len(vps))] for item
                              in sublist]

            closest_target = [target[i] for i in range(len(target)) if i in closest_target]
            pairing_lines = []

            for idx, vp in enumerate(vps):
                pairing_lines.append([vp.lat, vp.lon])
                pairing_lines.append([closest_target[idx].lat, closest_target[idx].lon])
                pairing_lines.append([None, None])

            figure["pairing_lines"] = pairing_lines

        # Find out if the indexed enemy targets are within range of GBADS
        gbads_in_range = [[j, list(targets_idx.intersection(ground_polygon[j].bounds))] for j in
                          range(len(ground_assets))]

        # Above list may contain different GBADS covering different enemy targets, get only unique GBADS
        unique_gbads = [item[0] for item in gbads_in_range if item[1]]

        # GBADS maximum range is a circle, rtree may have False Positives (FP) in this case as it expects perfect
        # hyper-rectangles (not circles). To cater FP, assert the detected GBADS by shapely within method.
        real_gbads = []
        for i in unique_gbads:
            if any([asset.within(ground_assets[i].get_range()[1]) for asset in targets]):
                real_gbads.append(i)

        # Get actual info of the unique GBADS from 'ground_assets'
        gbads = [ground_assets[i] for i in range(len(ground_assets)) if i in real_gbads]

        figure["gbads"] = gbads

        if gbads:
            # Display detected GBADS max ranges (circles) that have targets in their envelope
            max_zone_gbads = [item for sublist in [x.get_range()[0] for x in gbads] for item in sublist]

            figure["max_zone_gbads"] = max_zone_gbads

        # TODO Add appropriate names in in-range GBADS boundaries for correct hovering information.
        figure["vps"] = vps + vps_next
        # print(vps, vps_next)
        # print(figure.keys())

        return figure

    except StopIteration:
        print("Tracks list exhausted")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create a socket (SOCK_DGRAM means a UPD packet while SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server's up")
    # Bind the socket to the port
    server_address = (HOST, PORT)
    sock.bind(server_address)

    # target_data = pd.read_csv("C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/enemy/
    # enemy-airborne/tracks.csv")

    while True:
        print("Server is listening")
        recv_data = sock.recvfrom(4096)
        print(f"Client message: {recv_data[0]}")

        address = recv_data[1]

        data = iterate()
        data = pickle.dumps(data)
        # data = bytes(data, encoding="utf-8")

        print("Sending reply to the client")
        sock.sendto(data, address)
