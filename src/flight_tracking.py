# from dash import html, Dash, dcc, Input, Output, State
# import plotly.express as px
# import pandas as pd
# import dash
#
# import random
#
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     html.Div([html.H3('Extend multiple traces at once'),
#               dcc.Graph(id='graph-extendable-2',
#                         figure=dict(
#                             data=[{'x': [0, 1, 2, 3, 4],
#                                    'y': [0, .5, 1, .5, 0],
#                                    'mode': 'lines+markers'
#                                    },
#                                   {'x': [0, 1.1, 1.2, 1.3, 1.4],
#                                    'y': [0, 0, 0, 0, 0],
#                                    'mode': 'markers'
#                                    # 'mode': 'lines+markers'
#
#                                    }],
#                         )
#                         ),
#               ]),
#     dcc.Interval(
#         id='interval-graph-update',
#         interval=10000,
#         n_intervals=0),
# ])
#
#
# @app.callback(Output('graph-extendable-2', 'extendData'),
#               [Input('interval-graph-update', 'n_intervals')],
#               [State('graph-extendable-2', 'figure')])
# def update_extend_traces(n_intervals, existing):
#     x = (dict(x=[
#         [existing['data'][0]['x'][-1] + 1],
#         # [existing['data'][1]['x'][-1] + 1]
#     ],
#         y=[
#             [n_intervals * random.random()],
#             # [n_intervals * random.random()]
#         ]),
#          [0]
#     )
#     return x
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)


from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import dash
from shapely.ops import cascaded_union, unary_union
from synthetic_data.airborne import airborne_targets

import random

target_data = pd.read_csv("C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/enemy/enemy-airborne/tracks.csv")

app = dash.Dash(__name__)

fig = go.Figure(go.Scattermapbox(
    mode="lines",
    fill="toself",
    lat=[28.91, 28.9, 29.1, 29],
    lon=[71.9, 72, 71.8, 71.8],
))

# [74.262425, 33.999103]

fig.add_trace(go.Scattermapbox(
    mode="markers",
    lat=[33.999103],
    lon=[74.262425],
))

fig.update_layout(
    mapbox={'center': {'lat': 29.5, 'lon': 74, }, 'zoom': 5.2},
    showlegend=False,
    mapbox_style="white-bg",
)

all_targets = airborne_targets()

data0 = go.Scattermapbox(lat=[28.91, 28.9, 29.1, 29],
                         lon=[71.9, 72, 71.8, 71.8],
                         mode='lines',
                         fill='toself')

data1 = go.Scattermapbox(lat=[33.999103],
                         lon=[74.262425],
                         mode='markers',
                         marker={'size': 8}
                         )
# Draw dynamic range as a circle
data2 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],  # lower x1, x2 and upper x4, x3
    lon=[None],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(255, 255, 0, 0.3)', }  # Opacity of border color via alpha channel
)

# Draw dynamic range as a circle
data3 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(0, 255, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],  # lower x1, x2 and upper x4, x3
    lon=[None],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(0, 255, 255, 0.1)', }  # Opacity of border color via alpha channel
)

import random

N = 15

lat = [random.random() + 30 + random.random() for i in range(N)]
lon = [random.random() + 70 + random.random() for i in range(N)]

new_lat = []
for idx, ele in enumerate(lat):
    new_lat.append(ele)
    if idx != 0 and idx % 4 == 0:
        new_lat.append(new_lat[-4])
        new_lat.append(None)
new_lat.pop(0)

new_lon = []
for idx, ele in enumerate(lon):
    new_lon.append(ele)
    if idx != 0 and idx % 4 == 0:
        new_lon.append(new_lon[-4])
        new_lon.append(None)
new_lon.pop(0)

# Draw max ranges of all enemy targets as an individual circle
data4 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 255, 0.1)',  # Opacity of fill color via alpha channel
    lat=[new_lat],  # lower x1, x2 and upper x4, x3
    lon=[new_lon],  # lower y1, y2, and upper y4, y3
    # marker={'size': 8, 'color': 'rgba(255, 0, 255, 0.2)', }  # Opacity of border color via alpha channel
)

data = [data0, data1, data2, data3]

layout = dict(
    mapbox=dict(center=dict(lat=29.5, lon=74),
                style='carto-darkmatter',
                zoom=5.2))

# l = dict(
#     [{'center': {'lat': 29.5, 'lon': 74},
#              'zoom': 5.2,
#              'style': 'white-bg'
#              }],
# )

app.layout = html.Div([
    html.Div([html.H3('Extend single trace at once'),
              dcc.Graph(id='graph-extendable', figure=go.Figure(data=data, layout=layout),
                        style={'width': '100vw', 'height': '90vh'})]),
    dcc.Interval(id='interval-graph-update', interval=1 * 1000, n_intervals=0, max_intervals=15),
])


@app.callback(Output('graph-extendable', 'figure'),
              [Input('interval-graph-update', 'n_intervals')],
              [State('graph-extendable', 'figure')])
def update_extend_traces(n_intervals, existing):
    target = next(all_targets)

    # Initializing polygons for enemy air targets at current instance of time to be used in rtree collision
    # target_flat_polygon, target_polygon = zip(*[tar.get_range() for tar in target])
    # if n_intervals < len(target_data):

    target_flat_polygon, target_polygon = zip(*[tar.get_range() for tar in target])

    existing['data'][1]['lat'] = [x.lat for x in target]
    existing['data'][1]['lon'] = [x.lon for x in target]
    existing['data'][1]['text'] = [x.name for x in target]
    existing['data'][1]['hoverinfo'] = ['text' for x in range(len(target))]

    # max_range = [item for sublist in target_flat_polygon for item in sublist]
    # existing['data'][2]['lat'] = [x[1] for x in max_range]
    # existing['data'][2]['lon'] = [x[0] for x in max_range]

    combine_polygon = unary_union(target_polygon)
    combine_polygon = list(combine_polygon.exterior.coords)
    # combine_polygon.append([None, None])
    combine_polygon = [*combine_polygon]

    existing['data'][3]['lat'] = [x[1] for x in combine_polygon]
    existing['data'][3]['lon'] = [x[0] for x in combine_polygon]
    # existing['data'][3]['line'] = dict(shape='linear', color='rgb(10, 12, 240)', dash='dashdot')
    # existing['data'][3]['connectgaps '] = True

    # lon, lat = target_data.iloc[n_intervals, :]
    # existing['data'][1]['lat'] = [lat]
    # existing['data'][1]['lon'] = [lon]

    # existing['data'][1]['text'] = [x.name for x in target]
    # existing['data'][1]['hoverinfo'] = ['text' for x in range(len(target))]
    #
    # existing['data'][1] = []
    # if n_intervals < len(target_data):
    #     lon, lat = target_data.iloc[n_intervals, :]
    #     x = (dict(lat=[
    #         [lat],
    #     ],
    #         lon=[
    #             [lon],
    #         ]),
    #          [1]
    #     )
    # else:
    #     x = (dict(lat=[
    #         [33.999103],
    #     ],
    #         lon=[
    #             [74.262425],
    #         ]),
    #          [1]
    #     )
    return existing
    # return existing


if __name__ == '__main__':
    app.run_server(debug=True)

#
# import dash
# from dash import dcc, html
# import numpy as np
# import pandas as pd
# import json
# import plotly.express as px
# from dash.dependencies import Output, Input, State
#
# app = dash.Dash(__name__)
#
# locations = "\"{\\\"site_code\\\":{\\\"0\\\":\\\"0n110w\\\",\\\"1\\\":\\\"0n140w\\\",\\\"2\\\":\\\"0n165e\\\",\\\"3\\\":\\\"0n170w\\\",\\\"4\\\":\\\"0n23w\\\",\\\"5\\\":\\\"0n80.5e\\\",\\\"6\\\":\\\"0n95w\\\",\\\"7\\\":\\\"10n95w\\\",\\\"8\\\":\\\"10s10w\\\",\\\"9\\\":\\\"12n23w\\\",\\\"10\\\":\\\"12n95w\\\",\\\"11\\\":\\\"15n38w\\\",\\\"12\\\":\\\"15n65e\\\",\\\"13\\\":\\\"15n90e\\\",\\\"14\\\":\\\"19s34w\\\",\\\"15\\\":\\\"20n38w\\\",\\\"16\\\":\\\"2n95w\\\",\\\"17\\\":\\\"2s95w\\\",\\\"18\\\":\\\"3.5n95w\\\",\\\"19\\\":\\\"5n95w\\\",\\\"20\\\":\\\"5s95w\\\",\\\"21\\\":\\\"6s8e\\\",\\\"22\\\":\\\"8n95w\\\",\\\"23\\\":\\\"8s67e\\\",\\\"24\\\":\\\"8s95w\\\"},\\\"wmo_platform_code\\\":{\\\"0\\\":\\\"32323\\\",\\\"1\\\":\\\"51311\\\",\\\"2\\\":\\\"52321\\\",\\\"3\\\":\\\"51010\\\",\\\"4\\\":\\\"31007\\\",\\\"5\\\":\\\"23001\\\",\\\"6\\\":\\\"32321\\\",\\\"7\\\":\\\"43008\\\",\\\"8\\\":\\\"15001\\\",\\\"9\\\":\\\"13001\\\",\\\"10\\\":\\\"43011\\\",\\\"11\\\":\\\"13008\\\",\\\"12\\\":\\\"23011\\\",\\\"13\\\":\\\"23009\\\",\\\"14\\\":\\\"31005\\\",\\\"15\\\":\\\"41139\\\",\\\"16\\\":\\\"32320\\\",\\\"17\\\":\\\"32322\\\",\\\"18\\\":\\\"32011\\\",\\\"19\\\":\\\"32303\\\",\\\"20\\\":\\\"32304\\\",\\\"21\\\":\\\"15007\\\",\\\"22\\\":\\\"43301\\\",\\\"23\\\":\\\"14040\\\",\\\"24\\\":\\\"32305\\\"},\\\"latitude\\\":{\\\"0\\\":0.0,\\\"1\\\":0.0,\\\"2\\\":0.0,\\\"3\\\":0.0,\\\"4\\\":0.0,\\\"5\\\":0.0,\\\"6\\\":0.0,\\\"7\\\":10.0,\\\"8\\\":-10.0,\\\"9\\\":12.0,\\\"10\\\":12.0,\\\"11\\\":15.0,\\\"12\\\":15.0,\\\"13\\\":15.0,\\\"14\\\":-19.0,\\\"15\\\":20.0,\\\"16\\\":2.0,\\\"17\\\":-2.0,\\\"18\\\":3.5,\\\"19\\\":5.0,\\\"20\\\":-5.0,\\\"21\\\":-6.0,\\\"22\\\":8.0,\\\"23\\\":-8.0,\\\"24\\\":-8.0},\\\"longitude\\\":{\\\"0\\\":-110.0,\\\"1\\\":-140.0,\\\"2\\\":165.0,\\\"3\\\":-170.0,\\\"4\\\":-23.0,\\\"5\\\":80.5,\\\"6\\\":-95.0,\\\"7\\\":-95.0,\\\"8\\\":-10.0,\\\"9\\\":-23.0,\\\"10\\\":-95.0,\\\"11\\\":-38.0,\\\"12\\\":65.0,\\\"13\\\":90.0,\\\"14\\\":-34.0,\\\"15\\\":-38.0,\\\"16\\\":-95.0,\\\"17\\\":-95.0,\\\"18\\\":-95.0,\\\"19\\\":-95.0,\\\"20\\\":-95.0,\\\"21\\\":8.0,\\\"22\\\":-95.0,\\\"23\\\":67.0,\\\"24\\\":-95.0}}\""
#
# locs = json.loads(locations)
# df = pd.read_json(locs, dtype={'wmo_platform_code': str, 'latitude': np.float64, 'longitude': np.float64})
# menu_options = [{'label': platform, 'value': platform} for platform in sorted(df['wmo_platform_code'].to_list())]
# app.layout = html.Div(children=[
#     dcc.Graph(id='location-map'),
#     dcc.Dropdown(id='platforms-dd', options=menu_options, multi=True),
#     html.Div(id='hidden-div', style={'display': 'none'})
# ]
# )
#
#
# @app.callback(
#     Output("location-map", "figure"),
#     Input('hidden-div', 'children')
# )
# def show_map(adiv):
#
#     location_map = px.scatter_geo(df,
#                                   lat='latitude', lon='longitude',
#                                   color='wmo_platform_code',
#                                   custom_data=['wmo_platform_code'],
#                                   labels={'title': 'Platform'},
#                                   category_orders={'wmo_platform_code': sorted(df['wmo_platform_code'].to_list())},
#                                   )
#     location_map.update_layout(clickmode='select+event')
#     location_map.update_traces(marker_size=10,
#                                unselected=dict(marker=dict(size=10)),
#                                selected=dict(marker=dict(size=14))
#                                )
#
#     return location_map
#
#
# @app.callback(
#     Output('platforms-dd', 'value'),
#     Output('location-map', 'selectedData'),
#     Input('platforms-dd', 'value'),
#     Input('location-map', 'selectedData'),
#     Input('location-map', 'clickData'),
#     prevent_initial_call=True
# )
# def show_map(menu_values, selections, clicks):
#     ctx = dash.callback_context
#     oid = None
#     if ctx.triggered:
#         oid = ctx.triggered[0]['prop_id'].split('.')[0]
#     else:
#         print('call back with no trigger')
#
#     if oid == 'location-map':
#         # Map click, set the menu according to the map
#         menu_values = []
#         if clicks is not None:
#             if selections is not None:
#                 if 'points' in selections:
#                     for p in selections['points']:
#                         plat = p['customdata'][0]
#                         if plat not in menu_values:
#                             menu_values.append(plat)
#         print("Thissss")
#         print(str(menu_values))
#
#     else:  # The menu changed
#         remove = []
#         if selections is not None:
#             if 'points' in selections:
#                 for a_point in selections['points']:
#                     plat_selected = a_point['customdata'][0]
#                     if plat_selected not in menu_values:
#                         remove.append(a_point)
#             for r in remove:
#                 if r in selections['points']:
#                     selections['points'].remove(r)
#         print("Thatttt")
#         print(str(selections))
#
#     return menu_values, selections
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

#
# # Generate Random Rectangles
# import plotly.graph_objects as go
# import random
# import numpy as np
#
# # N = 1_00_000
# N = 10
#
# lat = [random.random() + 30 + random.random() + random.random() + np.random.randn() for i in range(N)]
# lon = [random.random() + 70 + random.random() + random.random() + np.random.randn() for i in range(N)]
#
# # fig = go.Figure()
#
#
# new_lat = []
# for idx, ele in enumerate(lat):
#     new_lat.append(ele)
#     if idx != 0 and idx % 4 == 0:
#         new_lat.append(new_lat[-4])
#         new_lat.append(None)
# new_lat.pop(0)
#
# new_lon = []
# for idx, ele in enumerate(lon):
#     new_lon.append(ele)
#     if idx != 0 and idx % 4 == 0:
#         new_lon.append(new_lon[-4])
#         new_lon.append(None)
# new_lon.pop(0)
#
# # Draw max ranges of all enemy targets as an individual circle
# data = go.Scatter(
#     mode="lines",
#     # fill="toself",
#     # fillcolor='rgba(0, 255, 0, 0.1)',  # Opacity of fill color via alpha channel
#     x=new_lat,  # lower x1, x2 and upper x4, x3
#     y=new_lon,  # lower y1, y2, and upper y4, y3
#     hoverinfo='skip',
#     # marker={'size': 8, 'color': 'rgba(255, 0, 255, 0.2)', }  # Opacity of border color via alpha channel
# )
#
# layout = go.Layout(
#         title=go.layout.Title(text="A Figure Specified By A Graph Object"))
#
# fig = go.Figure(data=data, layout=layout)
#
# if __name__ == '__main__':
#     fig.show()
