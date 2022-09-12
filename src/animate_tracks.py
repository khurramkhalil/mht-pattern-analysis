# from dash import html, dcc, Input, Output, State
# import plotly.graph_objects as go
# import pandas as pd
# import dash
# import random
#
# target_data = pd.read_csv("C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/enemy/enemy-airborne/tracks.csv")
#
# app = dash.Dash(__name__)
#
# fig = go.Figure(go.Scattermapbox(
#     mode="lines",
#     fill="toself",
#     lat=[28.91, 28.9, 29.1, 29],
#     lon=[71.9, 72, 71.8, 71.8],
# ))
#
# # [74.262425, 33.999103]
#
# fig.add_trace(go.Scattermapbox(
#     mode="markers",
#     lat=[33.999103],
#     lon=[74.262425],
# ))
#
# fig.update_layout(
#     mapbox={'center': {'lat': 29.5, 'lon': 74, }, 'zoom': 5.2},
#     showlegend=False,
#     mapbox_style="white-bg",
# )
#
# # data = [{'lat': [28.91, 28.9, 29.1, 29],
# #          'lon': [71.9, 72, 71.8, 71.8],
# #          'mode': 'lines',
# #          'fill': 'toself'
# #          },
# #         {'lat': [33.999103],
# #          'lon': [74.262425],
# #          'mode': 'markers'
# #          }]
# #
# # l = dict(
# #     layout=[{'center': {'lat': 29.5, 'lon': 74},
# #              'zoom': 5.2,
# #              'style': 'white-bg'
# #              }],
# # )
#
# data0 = go.Scattermapbox(lat=[28.91, 28.9, 29.1, 29],
#                          lon=[71.9, 72, 71.8, 71.8],
#                          mode='lines',
#                          fill='toself')
# data1 = go.Scattermapbox(lat=[33.999103],
#                          lon=[74.262425],
#                          mode='markers',
#                          marker={'size': 8}
#                          )
#
# data = [data0, data1]
#
# layout = dict(
#     mapbox=dict(center=dict(lat=29.5, lon=74),
#                 style='carto-darkmatter',
#                 zoom=5.2))
#
# # l = dict(
# #     [{'center': {'lat': 29.5, 'lon': 74},
# #              'zoom': 5.2,
# #              'style': 'white-bg'
# #              }],
# # )
#
# app.layout = html.Div([
#     html.Div([html.H3('Extend single trace at once'),
#               dcc.Graph(id='graph-extendable', figure=go.Figure(data=data, layout=layout),
#                         style={'width': '100vw', 'height': '90vh'})]),
#     dcc.Interval(id='interval-graph-update', interval=5 * 1000, n_intervals=0),
# ])
#
#
# @app.callback(Output('graph-extendable', 'extendData'),
#               [Input('interval-graph-update', 'n_intervals')],
#               [State('graph-extendable', 'figure')])
# def update_extend_traces(n_intervals, existing):
#     existing['data'][1] = []
#     if n_intervals < len(target_data):
#         lon, lat = target_data.iloc[n_intervals, :]
#         x = (dict(lat=[
#             [lat],
#         ],
#             lon=[
#                 [lon],
#             ]),
#              [1]
#         )
#     else:
#         x = (dict(lat=[
#             [33.999103],
#         ],
#             lon=[
#                 [74.262425],
#             ]),
#              [1]
#         )
#     return x
#     # return existing
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)


