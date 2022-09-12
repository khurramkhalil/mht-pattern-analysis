import plotly.graph_objects as go
import geojson
import geopandas as gpd
import fiona
import io


# import json

# from urllib.request import urlopen
# import json
#
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
# Import geojson boundaries


path = 'C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/boundaries/IBGEOJSON2.geojson'

with open(path) as f:
    df = geojson.load(f)



# def read_tracks_filtered(path):
#     src = fiona.open(path)
#     meta = src.meta
#     meta['driver'] = 'GeoJSON'
#
#     with io.BytesIO() as buffer:
#         with fiona.open(buffer, 'w', **meta) as dst:
#             for i, feat in enumerate(src):
#                 if len(feat['geometry']['coordinates'][0]) > 1:
#                     dst.write(feat)
#
#         buffer.seek(0)
#         df_ = gpd.read_file(buffer, driver='GeoJSON')
#
#     return df_
#
#
# df = read_tracks_filtered(path)

points = []

for feature in df["features"]:
    if feature['geometry']['type'] == 'Polygon':
        points.extend(feature['geometry']['coordinates'][0])
        points.append([None, None])  # mark the end of a polygon
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            points.extend(polyg[0])
            points.append([None, None])  # end of polygon
    elif feature['geometry']['type'] == 'MultiLineString':
        points.extend(feature['geometry']['coordinates'])
        points.append([None, None])
    else:
        pass

# lons, lats = zip(*points)

# Pakistan centered Geo map
fig = go.Figure(go.Scattermapbox(
    fill="toself",
    # lon=[-74, -70, -70, -74], lat=[47, 47, 45, 45],
    lat=[28, 28, 29, 29],  # lower x1, x2 and upper x4, x3
    lon=[71, 72, 72.1, 71.1],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': "orange"}))

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ])

fig.update_layout(
    mapbox={
        'center': {'lat': 29.5, 'lon': 74, },
        'zoom': 5.2},
    showlegend=False)

fig.show()

if __name__ == "__main__":
    pass

"""
import plotly.graph_objects as go

fig = go.Figure(go.Scattermapbox(
    mode="markers",
    lon=[-73.605], lat=[45.51],
    marker={'size': 20, 'color': ["cyan"]}))

fig.update_layout(
    mapbox={
        'style': "stamen-terrain",
        'center': {'lon': -73.6, 'lat': 45.5},
        'zoom': 12, 'layers': [{
            'source': {
                'type': "FeatureCollection",
                'features': [{
                    'type': "Feature",
                    'geometry': {
                        'type': "MultiPolygon",
                        'coordinates': [[[
                            [-73.606352888, 45.507489991], [-73.606133883, 45.50687600],
                            [-73.605905904, 45.506773980], [-73.603533905, 45.505698946],
                            [-73.602475870, 45.506856969], [-73.600031904, 45.505696003],
                            [-73.599379992, 45.505389066], [-73.599119902, 45.505632008],
                            [-73.598896977, 45.505514039], [-73.598783894, 45.505617001],
                            [-73.591308727, 45.516246185], [-73.591380782, 45.516280145],
                            [-73.596778656, 45.518690062], [-73.602796770, 45.521348046],
                            [-73.612239983, 45.525564037], [-73.612422919, 45.525642061],
                            [-73.617229085, 45.527751983], [-73.617279234, 45.527774160],
                            [-73.617304713, 45.527741334], [-73.617492052, 45.527498362],
                            [-73.617533258, 45.527512253], [-73.618074188, 45.526759105],
                            [-73.618271651, 45.526500673], [-73.618446320, 45.526287943],
                            [-73.618968507, 45.525698560], [-73.619388002, 45.525216750],
                            [-73.619532966, 45.525064183], [-73.619686662, 45.524889290],
                            [-73.619787038, 45.524770086], [-73.619925742, 45.524584939],
                            [-73.619954486, 45.524557690], [-73.620122362, 45.524377961],
                            [-73.620201713, 45.524298907], [-73.620775593, 45.523650879]
                        ]]]
                    }
                }]
            },
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

fig.show()
"""

"""
import plotly.graph_objects as go

# Geomap with multiple boxes (three) of different sizes on different regions.
fig = go.Figure(go.Scattermapbox(
    mode="lines", fill="toself",
    lon=[-10, -10, 8, 8, -10, None, 30, 30, 50, 50, 30, None, 100, 100, 80, 80, 100],
    lat=[30, 6, 6, 30, 30, None, 20, 30, 30, 20, 20, None, 40, 50, 50, 40, 40]))

fig.update_layout(
    mapbox={'style': "stamen-terrain", 'center': {'lon': 30, 'lat': 30}, 'zoom': 2},
    showlegend=False,
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

fig.show()

"""
