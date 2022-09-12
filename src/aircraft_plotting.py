import plotly.graph_objects as go
from shapely.geometry import Point
from international_border import load_boundaries
from pakistan_polygon import load_polygon
from geom_calculations import dynamic_arc
from synthetic_data.gbads import ground_assets
from synthetic_data.trace_track import path_generator
from synthetic_data.vps import vital_points
# from geom_calculations import dynamic_range

# STATIC ITEMS
# Indian occupied Kashmir data
iok_bound = load_boundaries([6, 7])

# Pakistan centered Geo map
pak_bound = load_boundaries()

# Pakistan polygon
pak_polygon = load_polygon()

# DYNAMIC ITEMS
# Friendly GBADS
ground_assets = ground_assets()

# VP data points
vp_points = vital_points()

# Enemy Targets
targets = [
    Point([74.262425, 33.999103]),
    Point([74.874538, 31.618451]),
    Point([73.168699, 26.098721]),
    Point([77.339297, 27.024877]),
            ]

# Initializing Figure
fig = go.Figure(go.Scattermapbox(
    mode="lines",
    fill="toself",
    lat=[28.91, 28.9, 29.1, 29],  # lower x1, x2 and upper x4, x3
    lon=[71.9, 72, 71.8, 71.8],  # lower y1, y2, and upper y4, y3
    # marker={'size': 8, 'color': "orange"}
))

# Plotting IoK bounds

fig.add_trace(go.Scattermapbox(
    mode="lines",
    lat=[x[1] for x in iok_bound],
    lon=[x[0] for x in iok_bound],
    marker={'size': 20, 'color': "black"},
    text="IOK",
    hoverinfo="text"))

# Plotting Pakistan bounds

fig.add_trace(go.Scattermapbox(
    mode="lines",
    lat=[x[1] for x in pak_bound],
    lon=[x[0] for x in pak_bound],
    marker={'size': 20, 'color': "green"},
    text="PAK IB",
    hoverinfo="text"
))

# Plotting test points based on fact if they lie inside Pakistan or outside. Depending on results, assign appropriate
# color and if needed draw a load out circle with different fill-color and border color and their opacities.

color = 'blue'
fig.add_trace(go.Scattermapbox(
    mode="markers",
    lat=[point.lat for point in ground_assets],
    lon=[point.lon for point in ground_assets],
    marker=go.scattermapbox.Marker(
        size=8,
        color=color
    ),
    text=[point.name for point in ground_assets],
    hoverinfo="text",
))

# Calculate dynamic range of the current weapon system (declared by range_ parameter) as a circle
dynamic_circle = [item for sublist in [x.get_range() for x in ground_assets] for item in sublist]

# Draw dynamic range as a circle
fig.add_trace(go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(0, 0, 255, 0.1)',        # Opacity of fill color via alpha channel
    lat=[x[1] for x in dynamic_circle],  # lower x1, x2 and upper x4, x3
    lon=[x[0] for x in dynamic_circle],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(0, 0, 255, 0.5)', }     # Opacity of border color via alpha channel
))


# Calculate dynamic range of the current weapon system (declared by range_ parameter) as a circle
kill_circle = [item for sublist in [kill.kill_zone for kill in ground_assets] for item in sublist]

# Draw dynamic range as a circle
fig.add_trace(go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 0, 0.1)',        # Opacity of fill color via alpha channel
    lat=[x[1] for x in kill_circle],  # lower x1, x2 and upper x4, x3
    lon=[x[0] for x in kill_circle],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(255, 0, 0, 0.2)', }     # Opacity of border color via alpha channel
))

for point in targets:
    if not pak_polygon.contains(point):
        color = 'red'

        # Add point itself as a circle with some size and color
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lat=[point.y],
            lon=[point.x],
            marker=go.scattermapbox.Marker(
                size=8,
                color=color
            ),
            text=[color],
            hoverinfo="text",
        ))

        # Calculate dynamic range of the current weapon system (as identified) as an arc
        arc_sector = dynamic_arc(point)
        la = [x[1] for x in arc_sector]
        lo = [x[0] for x in arc_sector]

        # Draw dynamic range as an arc
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            fill="toself",
            fillcolor='rgba(255, 0, 0, 0.3)',        # Opacity of fill color via alpha channel
            lat=la,  # lower x1, x2 and upper x4, x3
            lon=lo,  # lower y1, y2, and upper y4, y3
            marker={'size': 8, 'color': 'rgba(0, 255, 0, 0.2)', }     # Opacity of border color via alpha channel
        ))


# Plotting vp points in a single trace
color = 'yellow'
fig.add_trace(go.Scattermapbox(
    mode="markers",
    # marker_symbol="square",
    lat=[point.lat for point in vp_points],
    lon=[point.lon for point in vp_points],
    marker=go.scattermapbox.Marker(
        size=[point.size for point in vp_points],
        color=color
    ),
    text=[point.name for point in vp_points],
    hoverinfo="text",
))

# arr = path_generator(74.289496, 75.886611, 33.936026, 33.938269, 20, 20)
track_0 = path_generator(74.289496, 74.964219, 33.936026, 34.033505, 20, 20)
track_1 = path_generator(76.689822, 74.581955, 30.764456, 30.995465, 30, 12)

tracks = [track_0, track_1]

for track in tracks:
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lat=[x[1] for x in track],
        lon=[x[0] for x in track],
        marker={'size': 8, 'color': "indigo"},
    ))

# Setting map type and properties
fig.update_layout(
    mapbox={'center': {'lat': 29.5, 'lon': 74, }, 'zoom': 5.2},
    showlegend=False,

    # mapbox_style="white-bg",          # Plane White Background
    # mapbox_style="stamen-terrain",  # Light White Map
    mapbox_style="carto-darkmatter",  # Black Map
    # mapbox_style="open-street-map",        # Open Street Map
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ]
)

# fig.data[1]['visible'] = False
fig.show()

if __name__ == "__main__":
    pass


# Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'extendData'),
#               [Input('interval-component', 'n_intervals')],
#               [State('live-update-graph', 'figure')])
# def update_graph_live(n_intervals, existing):
#     # if n_intervals < len(target_data):
#     lon, lat = target_data.iloc[n_intervals, :]
#     x = (dict(lat=[
#         [lat, None, lat + 0.2, None, lat + 0.4, None, lat - 0.2, None, lat - 0.4],
#     ],
#         lon=[
#             [lon, None, lon + 0.2, None, lon + 0.4, None, lon - 0.2, None, lon - 0.4],
#         ],
#         # visible=False
#     ),
#          [6]
#     )
#     return x


# @app.callback(
#     Output("interval-component", "disabled"),
#     [Input("interval-component", "n_intervals")],
#     [State("interval-component", "disabled")],
# )
# def toggle_interval(n_intervals, disabled):
#     if n_intervals > len(target_data):
#         return not disabled
#     return disabled


# layout = dict(
#     mapbox=dict(center=dict(lat=29.5, lon=74),
#                 layers=(dict(below='traces'),
#                             dict(source=[
#                                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"]),
#                             dict(sourceattribution='United States Geological Survey'),
#                             dict(sourcetype='raster')),
#                 style='carto-darkmatter',
#                 zoom=5.2))


"""
# Setting map type and properties
fig.update_layout(
    mapbox={'center': {'lat': 29.5, 'lon': 74, }, 'zoom': 5.2},
    showlegend=False,

    mapbox_style="white-bg",          # Plane White Background
    # mapbox_style="stamen-terrain",  # Light White Map
    # mapbox_style="carto-darkmatter",  # Black Map
    # mapbox_style="open-street-map",        # Open Street Map
    # mapbox_layers=[
    #     {
    #         "below": 'traces',
    #         "sourcetype": "raster",
    #         "sourceattribution": "United States Geological Survey",
    #         "source": [
    #             "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #         ]
    #     }
    # ]
)
"""